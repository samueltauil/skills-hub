"""Finds the Cloud Billing BigQuery export and reads Cloud Logging costs."""

import collections
import concurrent.futures
import dataclasses
import datetime
import functools
import re
import time
from typing import Any, Dict, Iterator, List, Optional, Tuple

import attribution
from constants import DEFAULT_ANALYSIS_MONTHS
from constants import INGESTION_PRICING_UNIT
from constants import INGESTION_SKU_NAME
from constants import INVOICE_TIMEZONE
from constants import LOGGING_SCOPE_SQL
from constants import LOGGING_SERVICE_ID
from constants import LOGGING_SERVICE_NAME
from constants import quote_table_ref
import google.auth
from google.cloud import bigquery
import googleapiclient.discovery
from pricing import sku_of_description

# Billing modes, keyed on what the caller knows about the export's location:
#   `explicit` probe the named table/scope only.
#   `none`     no export; skip discovery and use list pricing.
#   `search`   this project, then the whole billing account.
MODE_NONE = "none"
MODE_EXPLICIT = "explicit"
MODE_SEARCH = "search"
BILLING_MODES = (MODE_NONE, MODE_EXPLICIT, MODE_SEARCH)

# Outcomes recorded per tier in `fallback_chain`. `inconclusive` means
# something could not be read, so an export may still exist (SKILL.md 3A).
FOUND = "found"
NO_PROJECT_RECORDS = "no_project_records"
NOT_FOUND = "not_found"
INCONCLUSIVE = "inconclusive"
SKIPPED = "skipped"

BILLING_EXPORT_PREFIXES = (
    "gcp_billing_export_v1_",
    "gcp_billing_export_resource_v1_",
)
_CAI_TABLE_RE = re.compile(
    r"//bigquery\.googleapis\.com/projects/([^/]+)/datasets/([^/]+)/tables/(.+)"
)

# `list_tables` defaults to 50 rows per request and pages within a dataset are
# sequential, so page size bounds the scan of a date-sharded dataset.
TABLE_LIST_PAGE_SIZE = 1000
DATASET_SCAN_WORKERS = 16
PROJECT_SCAN_WORKERS = 12
SCAN_PROGRESS_INTERVAL_SECONDS = 30.0
LARGE_PROJECT_DATASET_COUNT = 25
SLOW_SCAN_ADVISORY_SECONDS = 20.0

_SCOPE_SQL = (
    LOGGING_SCOPE_SQL.format(
        service_name="@service_name",
        service_id="@service_id",
        project_id="@project_id",
    )
    + f"\n  AND DATE(usage_start_time, '{INVOICE_TIMEZONE}') >= @window_start"
)

_NO_EXPORT_METADATA = {
    "status": "disabled",
    "table_name": None,
    "days_available": 0.0,
    "earliest_date": None,
    "latest_date": None,
    "currency": "USD",
    "distinct_months": 0,
}


@dataclasses.dataclass
class BillingResult:
  """Where costs came from. `costs` is None under list pricing."""

  costs: Optional[Dict[str, Any]]
  metadata: Dict[str, Any]
  chain: List[Dict[str, str]]

  @property
  def invoiced(self) -> bool:
    return self.costs is not None

  def summary(self) -> Dict[str, Any]:
    """The summary's `billing_metadata` block."""
    return {
        "invoiced": self.invoiced,
        **self.metadata,
        "fallback_chain": self.chain,
    }


@dataclasses.dataclass
class Scan:
  """Candidate tables from one search tier.

  `complete` is False when something could not be read, so an empty result
  does not prove there is no export.
  """

  tables: List[str]
  complete: bool = True
  detail: str = ""


def _export_rank(table: str) -> int:
  # The standard export is preferred over the resource-level one.
  return 0 if "gcp_billing_export_v1_" in table else 1


def _export_tables_in_dataset(
    bq_client: bigquery.Client,
    project: str,
    dataset_id: str,
    account_filter: Optional[str] = None,
) -> Optional[List[str]]:
  """Returns quoted export tables in one dataset, or None if unreadable."""
  try:
    return [
        f"`{project}.{dataset_id}.{t.table_id}`"
        for t in bq_client.list_tables(
            f"{project}.{dataset_id}", page_size=TABLE_LIST_PAGE_SIZE
        )
        if t.table_id.startswith(BILLING_EXPORT_PREFIXES)
        and (not account_filter or account_filter in t.table_id)
    ]
  except Exception:  # pylint: disable=broad-except
    return None


def scan_project_for_export_tables(
    bq_client: bigquery.Client,
    project: str,
    account_filter: Optional[str] = None,
    announce: bool = False,
) -> Scan:
  """Lists every dataset of `project` in parallel for export tables.

  BigQuery has no server-side table name filter, so the whole project is
  enumerated.

  Args:
    bq_client: BigQuery client.
    project: project to scan.
    account_filter: billing account ID export table names must contain.
    announce: print the cost of a slow scan (for the audited project).

  Returns:
    The export tables found, standard export first.
  """
  try:
    dataset_ids = [
        ds.dataset_id for ds in bq_client.list_datasets(project=project)
    ]
  except Exception as e:  # pylint: disable=broad-except
    return Scan([], False, f"Could not list the datasets of '{project}': {e}")
  if not dataset_ids:
    return Scan([], True, f"Project '{project}' has no datasets.")
  if announce and len(dataset_ids) >= LARGE_PROJECT_DATASET_COUNT:
    print(
        f"[BILLING DISCOVERY] Listing {len(dataset_ids)} datasets in"
        f" '{project}' to find the billing export. Passing --billing-table"
        " skips this search (~2s); --billing-mode=none skips it too."
    )

  started = time.monotonic()
  found: List[str] = []
  complete = True
  with concurrent.futures.ThreadPoolExecutor(
      max_workers=min(DATASET_SCAN_WORKERS, len(dataset_ids))
  ) as executor:
    for tables in executor.map(
        lambda ds: _export_tables_in_dataset(
            bq_client, project, ds, account_filter
        ),
        dataset_ids,
    ):
      if tables is None:
        complete = False
      else:
        found.extend(tables)
  elapsed = time.monotonic() - started
  if announce and elapsed >= SLOW_SCAN_ADVISORY_SECONDS:
    print(
        "[FINOPS ADVISORY - BILLING SYNC] Searching"
        f" {len(dataset_ids)} datasets in '{project}' took {elapsed:.0f}s"
        " because the export's location is unknown. Pass --billing-table next"
        " time, or --billing-mode=none if there is no export."
    )

  found.sort(key=_export_rank)
  if complete:
    return Scan(found, True, f"No billing export table in '{project}'.")
  return Scan(found, False, f"Some datasets of '{project}' could not be read.")


def _scan_projects_for_export(
    bq_client: bigquery.Client, projects: List[str], account_filter: str
) -> Tuple[Optional[str], int]:
  """Returns `(first export table found, unreadable count)` over `projects`."""
  # A None table proves no export only if `unreadable` is 0.
  started = last_progress = time.monotonic()
  unreadable = 0
  executor = concurrent.futures.ThreadPoolExecutor(
      max_workers=PROJECT_SCAN_WORKERS
  )
  try:
    futures = [
        executor.submit(
            scan_project_for_export_tables, bq_client, p, account_filter
        )
        for p in projects
    ]
    for done, future in enumerate(concurrent.futures.as_completed(futures), 1):
      scan = future.result()
      if scan.tables:
        return scan.tables[0], unreadable
      if not scan.complete:
        unreadable += 1
      now = time.monotonic()
      if now - last_progress >= SCAN_PROGRESS_INTERVAL_SECONDS:
        last_progress = now
        print(
            f"[BILLING DISCOVERY] Searched {done}/{len(futures)} projects on"
            f" the billing account ({now - started:.0f}s), no export yet."
        )
  finally:
    # A `with` block would wait for every running scan on an early return.
    executor.shutdown(wait=False, cancel_futures=True)
  return None, unreadable


def _discovery_credentials(bq_client: bigquery.Client) -> Any:
  # Without the ADC quota project, so these APIs need not be enabled on it
  # (SERVICE_DISABLED otherwise).
  creds = getattr(bq_client, "_credentials", None)
  if creds is None:
    creds, _ = google.auth.default()
  if hasattr(creds, "with_quota_project"):
    creds = creds.with_quota_project(None)
  return creds


def _org_scope(crm: Any, project_id: str) -> str:
  """Returns the project's organization, or the highest readable ancestor."""
  scope = f"projects/{project_id}"
  try:
    scope = crm.projects().get(name=scope).execute().get("parent") or scope
    while scope.startswith("folders/"):
      parent = crm.folders().get(name=scope).execute().get("parent")
      if not parent or parent == scope:
        break
      scope = parent
  except Exception as e:  # pylint: disable=broad-except
    print(f"Notice: Resource Manager scope resolution encountered: {e}")
  return scope


def _search_asset_inventory(
    build: Any, project_id: str, account_id: str
) -> Optional[str]:
  """One Cloud Asset Inventory search; often denied, hence only a fast path."""
  try:
    scope = _org_scope(build("cloudresourcemanager", "v3"), project_id)
    response = (
        build("cloudasset", "v1")
        .resources()
        .searchAll(
            scope=scope,
            query=" OR ".join(
                f"name:{prefix}{account_id}"
                for prefix in BILLING_EXPORT_PREFIXES
            ),
            assetTypes=["bigquery.googleapis.com/Table"],
        )
        .execute()
    )
  except Exception as e:  # pylint: disable=broad-except
    print(f"Notice: Cloud Asset Inventory search encountered: {e}")
    return None
  tables = []
  for item in response.get("results", []):
    match = _CAI_TABLE_RE.match(item.get("name", ""))
    if match and match.group(3).startswith(BILLING_EXPORT_PREFIXES):
      tables.append("`{}.{}.{}`".format(*match.groups()))
  return min(tables, key=_export_rank) if tables else None


def discover_account_export(
    bq_client: bigquery.Client, project_id: str
) -> Scan:
  """Finds the export anywhere on the billing account of `project_id`."""
  # Cloud Asset Inventory first, then every other project on the account.
  try:
    build = functools.partial(
        googleapiclient.discovery.build,
        credentials=_discovery_credentials(bq_client),
        cache_discovery=False,
        requestBuilder=attribution.discovery_request_builder(
            attribution.COLLECT_LOGGING_DATA
        ),
    )
    billing_svc = build("cloudbilling", "v1")
    info = (
        billing_svc.projects()
        .getBillingInfo(name=f"projects/{project_id}")
        .execute()
    )
  except Exception as e:  # pylint: disable=broad-except
    return Scan([], False, f"Could not read the project's billing account: {e}")
  account = info.get("billingAccountName")
  if not account or not info.get("billingEnabled", True):
    return Scan([], True, f"Billing is not enabled for '{project_id}'.")
  account_id = account.split("/")[-1].replace("-", "_")

  table = _search_asset_inventory(build, project_id, account_id)
  if table:
    return Scan([table])

  try:
    projects = []
    accounts = billing_svc.billingAccounts().projects()
    request = accounts.list(name=account, pageSize=100)
    while request is not None:
      response = request.execute()
      projects += [
          p["projectId"]
          for p in response.get("projectBillingInfo", [])
          if p.get("billingEnabled", True)
          and p.get("projectId") not in (None, project_id)
      ]
      request = accounts.list_next(request, response)
  except Exception as e:  # pylint: disable=broad-except
    return Scan([], False, f"Could not list the projects on '{account}': {e}")
  if not projects:
    return Scan([], True, "The billing account has no other projects.")

  print(
      f"[BILLING DISCOVERY] Searching all {len(projects)} projects on billing"
      f" account '{account}'. This runs until it finds an export or has"
      " checked every project, reporting progress every"
      f" {SCAN_PROGRESS_INTERVAL_SECONDS:.0f}s."
  )
  table, unreadable = _scan_projects_for_export(bq_client, projects, account_id)
  if table:
    return Scan([table])
  if unreadable:
    return Scan(
        [],
        False,
        f"Searched {len(projects)} projects on the billing account, but"
        f" {unreadable} could not be fully read, so an export these"
        " credentials cannot see may still exist.",
    )
  return Scan(
      [],
      True,
      f"Searched all {len(projects)} projects on the billing account without"
      " finding an export table.",
  )


def _candidates(
    bq_client: bigquery.Client,
    project_id: str,
    override_table: Optional[str],
    billing_project: Optional[str],
    billing_dataset: Optional[str],
) -> Iterator[Tuple[str, Scan]]:
  """Yields `(tier, scan)` in search order; later tiers run only if needed."""
  if override_table:
    yield "explicit_table", Scan([quote_table_ref(override_table)])
    return
  if billing_project or billing_dataset:
    target = billing_project or project_id
    if billing_dataset:
      tables = _export_tables_in_dataset(bq_client, target, billing_dataset)
      where = f"'{target}.{billing_dataset}'"
      yield "explicit_scope", Scan(
          tables or [],
          tables is not None,
          f"Could not list {where}."
          if tables is None
          else f"No billing export table in {where}.",
      )
    else:
      yield "explicit_scope", scan_project_for_export_tables(bq_client, target)
    return
  yield "local_project", scan_project_for_export_tables(
      bq_client, project_id, announce=True
  )
  yield "billing_account", discover_account_export(bq_client, project_id)


def _record(
    chain: List[Dict[str, str]],
    tier: str,
    status: str,
    detail: str,
    table: Optional[str] = None,
) -> None:
  step = {"tier": tier, "status": status, "detail": detail}
  if table:
    step["table"] = table
  chain.append(step)
  print(
      f"[BILLING DISCOVERY] {tier}: {status}"
      + (f" ({table})" if table else "")
      + f" - {detail}"
  )


def resolve_billing_source(
    bq_client: bigquery.Client,
    project_id: str,
    override_table: Optional[str] = None,
    billing_project: Optional[str] = None,
    billing_dataset: Optional[str] = None,
    analysis_months: int = DEFAULT_ANALYSIS_MONTHS,
    now: Optional[datetime.datetime] = None,
    billing_mode: str = MODE_SEARCH,
) -> BillingResult:
  """Reads costs from the first candidate table holding this project's rows.

  A named table or scope is the only candidate (whatever the mode); otherwise
  `search` tries this project, then the billing account.

  Args:
    bq_client: BigQuery client.
    project_id: audited project.
    override_table: export table named by the user.
    billing_project: project named by the user to search.
    billing_dataset: dataset named by the user to search.
    analysis_months: whole calendar months to read.
    now: current time; defaults to now (UTC).
    billing_mode: one of `BILLING_MODES`.

  Returns:
    The costs (None under list pricing), metadata and fallback chain.
  """
  now = now or datetime.datetime.now(datetime.timezone.utc)
  chain: List[Dict[str, str]] = []
  named = override_table or billing_project or billing_dataset
  if billing_mode == MODE_NONE and not override_table:
    _record(
        chain,
        "user_declared_no_export",
        SKIPPED,
        "Told there is no billing export, so nothing was searched.",
    )
    return BillingResult(None, dict(_NO_EXPORT_METADATA), chain)
  if billing_mode == MODE_EXPLICIT and not named:
    _record(
        chain,
        "explicit_scope",
        SKIPPED,
        "Explicit mode named no table, project or dataset to probe.",
    )
    return BillingResult(None, dict(_NO_EXPORT_METADATA), chain)

  for tier, scan in _candidates(
      bq_client, project_id, override_table, billing_project, billing_dataset
  ):
    for table in scan.tables:
      try:
        costs = query_logging_billing_costs(
            bq_client, table, project_id, analysis_months, now
        )
      except Exception as e:  # pylint: disable=broad-except
        _record(chain, tier, INCONCLUSIVE, f"Query failed: {e}", table)
        continue
      if costs["monthly_costs"]:
        _record(chain, tier, FOUND, "Reading costs from this table.", table)
        metadata = _metadata(costs, table, now, analysis_months)
        return BillingResult(costs, metadata, chain)
      _record(
          chain,
          tier,
          NO_PROJECT_RECORDS,
          f"Holds no Cloud Logging rows for '{project_id}'.",
          table,
      )
    if not scan.tables or not scan.complete:
      _record(
          chain,
          tier,
          NOT_FOUND if scan.complete else INCONCLUSIVE,
          scan.detail,
      )
  return BillingResult(None, dict(_NO_EXPORT_METADATA), chain)


def _window_start(
    now: datetime.datetime, analysis_months: int
) -> datetime.date:
  """First day of the oldest of `analysis_months` whole calendar months."""
  year, month = divmod(now.year * 12 + now.month - analysis_months, 12)
  return datetime.date(year, month + 1, 1)


def _metadata(
    costs: Dict[str, Any],
    table: str,
    now: datetime.datetime,
    analysis_months: int,
) -> Dict[str, Any]:
  """Describes the export's history from the rows the cost query returned."""
  dates = sorted(costs["daily_costs"])
  earliest = datetime.datetime.fromisoformat(dates[0]).replace(
      tzinfo=datetime.timezone.utc
  )
  # The query never reads before the window, so an export that reaches its
  # first day is as mature as this analysis can see.
  covers_window = dates[0] <= _window_start(now, analysis_months).isoformat()
  return {
      "status": "mature" if covers_window else "partial_window",
      "table_name": table,
      "days_available": round(
          max((now - earliest).total_seconds(), 0) / 86400, 1
      ),
      "earliest_date": dates[0],
      "latest_date": dates[-1],
      "currency": costs["currency"],
      "distinct_months": len(costs["monthly_costs"]),
  }


def query_logging_billing_costs(
    bq_client: bigquery.Client,
    table_name: str,
    project_id: str,
    analysis_months: int = DEFAULT_ANALYSIS_MONTHS,
    now: Optional[datetime.datetime] = None,
) -> Dict[str, Any]:
  """Returns monthly and daily Cloud Logging costs from the billing export.

  Dates are bucketed in Pacific time to match invoice months.

  Args:
    bq_client: BigQuery client.
    table_name: billing export table.
    project_id: project whose rows are read.
    analysis_months: whole calendar months to read.
    now: current time; defaults to now (UTC).

  Returns:
    Dict with `monthly_costs`, `daily_costs`, `daily_gib`, `daily_gib_by_sku`
    and `currency`. `monthly_costs` is empty when the table holds no rows for
    `project_id`.
  """
  now = now or datetime.datetime.now(datetime.timezone.utc)
  sql = f"""
  SELECT
    FORMAT_DATE('%Y-%m', DATE(usage_start_time, '{INVOICE_TIMEZONE}'))
      AS invoice_month,
    FORMAT_DATE('%Y-%m-%d', DATE(usage_start_time, '{INVOICE_TIMEZONE}'))
      AS usage_date,
    sku.description AS sku_description,
    currency,
    usage.pricing_unit AS pricing_unit,
    SUM(cost) AS raw_cost,
    SUM(IFNULL((SELECT SUM(c.amount) FROM UNNEST(credits) c), 0))
      AS total_credits,
    SUM(cost + IFNULL((SELECT SUM(c.amount) FROM UNNEST(credits) c), 0))
      AS net_cost,
    SUM(usage.amount_in_pricing_units) AS usage_amount
  FROM {quote_table_ref(table_name)}
  WHERE {_SCOPE_SQL}
  GROUP BY invoice_month, usage_date, sku_description, currency, pricing_unit
  ORDER BY usage_date ASC
  """
  job_config = bigquery.QueryJobConfig(
      query_parameters=[
          bigquery.ScalarQueryParameter(
              "service_name", "STRING", LOGGING_SERVICE_NAME
          ),
          bigquery.ScalarQueryParameter(
              "service_id", "STRING", LOGGING_SERVICE_ID
          ),
          bigquery.ScalarQueryParameter("project_id", "STRING", project_id),
          bigquery.ScalarQueryParameter(
              "window_start", "DATE", _window_start(now, analysis_months)
          ),
      ]
  )
  rows = list(bq_client.query(sql, job_config=job_config).result())

  monthly = collections.defaultdict(
      lambda: {
          "raw_cost": 0.0,
          "credits": 0.0,
          "net_cost": 0.0,
          "ingestion_gib": 0.0,
          "ingestion_raw_cost": 0.0,
          "ingestion_net_cost": 0.0,
          "sku_breakdown": collections.defaultdict(float),
          "ingestion_by_sku": collections.defaultdict(
              lambda: {"gib": 0.0, "raw_cost": 0.0, "net_cost": 0.0}
          ),
          "dates": set(),
      }
  )
  daily_costs: Dict[str, float] = collections.defaultdict(float)
  # Invoiced daily volume; preferred over `billing/bytes_ingested`, which can
  # silently under-report.
  daily_gib: Dict[str, float] = collections.defaultdict(float)
  daily_gib_by_sku: Dict[str, Dict[str, float]] = collections.defaultdict(
      lambda: collections.defaultdict(float)
  )
  for r in rows:
    day = r["usage_date"]
    sku = r["sku_description"] or INGESTION_SKU_NAME
    net = float(r["net_cost"] or 0.0)
    raw = float(r["raw_cost"] or 0.0)
    usage = float(r["usage_amount"] or 0.0)
    entry = monthly[r["invoice_month"]]
    entry["raw_cost"] += raw
    entry["credits"] += float(r["total_credits"] or 0.0)
    entry["net_cost"] += net
    entry["sku_breakdown"][sku] += net
    entry["dates"].add(day)
    daily_costs[day] += net
    # Ingestion only: retention rows (`gibibyte month`) would double-count.
    if (r["pricing_unit"] or "").strip().lower() == INGESTION_PRICING_UNIT:
      entry["ingestion_gib"] += usage
      entry["ingestion_raw_cost"] += raw
      entry["ingestion_net_cost"] += net
      daily_gib[day] += usage
      # SKUs differ in unit price and free tier, so price per SKU.
      sku_key = sku_of_description(sku)
      by_sku = entry["ingestion_by_sku"][sku_key]
      by_sku["gib"] += usage
      by_sku["raw_cost"] += raw
      by_sku["net_cost"] += net
      daily_gib_by_sku[sku_key][day] += usage

  return {
      "monthly_costs": {
          m: {
              "raw_cost_usd": round(v["raw_cost"], 2),
              "credits_usd": round(v["credits"], 2),
              "net_cost_usd": round(v["net_cost"], 2),
              "ingestion_gib": round(v["ingestion_gib"], 2),
              "ingestion_raw_cost_usd": round(v["ingestion_raw_cost"], 2),
              "ingestion_net_cost_usd": round(v["ingestion_net_cost"], 2),
              "billed_days": len(v["dates"]),
              "sku_breakdown": {
                  k: round(c, 2) for k, c in v["sku_breakdown"].items()
              },
              "ingestion_by_sku": {
                  k: {
                      "gib": round(s["gib"], 2),
                      "raw_cost_usd": round(s["raw_cost"], 2),
                      "net_cost_usd": round(s["net_cost"], 2),
                  }
                  for k, s in v["ingestion_by_sku"].items()
              },
          }
          for m, v in monthly.items()
      },
      "daily_costs": {d: round(v, 2) for d, v in daily_costs.items()},
      # 4dp so a tiny billed day doesn't round to zero.
      "daily_gib": {d: round(v, 4) for d, v in daily_gib.items()},
      "daily_gib_by_sku": {
          sku: {d: round(v, 4) for d, v in days.items()}
          for sku, days in daily_gib_by_sku.items()
      },
      "currency": (rows[0]["currency"] if rows else None) or "USD",
  }
