"""Builds the "Prove It" provenance for every headline number in the report.

Pure function of the summary dict: each claim gets its formula, sources with
console links, known differences, and checks that `verify_claim.py` re-runs.
Queries are literal text (no `@params`). SQL and PromQL checks run exactly the
query their drawer shows; stream checks use the Monitoring filter the collector
measured with.
"""

import datetime
import json
import re
from typing import Any, Dict, List, Optional, Sequence, Tuple
import urllib.parse

from actions import SOURCE_LEVER
from constants import bare_table_ref
from constants import BILLED_BYTES_METRIC
from constants import BYTE_COUNT_METRIC
from constants import BYTES_PER_GIB
from constants import DAYS_PER_MONTH
from constants import DEFAULT_SAMPLE_DAYS
from constants import DEFAULT_TELEMETRY_LOOKBACK_DAYS
from constants import INGESTION_PRICING_UNIT
from constants import INVOICE_TIMEZONE
from constants import LOGGING_SCOPE_SQL
from constants import LOGGING_SERVICE_ID
from constants import LOGGING_SERVICE_NAME
from constants import MONITORING_RETENTION_DAYS
from constants import PAYLOAD_BYTES_SQL
from constants import quote_table_ref
from pricing import BLENDED
from pricing import last_complete_invoice_day
from pricing import LOG_STORAGE
from pricing import PriceBook
from pricing import SKU_LABELS
from pricing import sku_of_resource
from pricing import SkuTerms
from pricing import VENDED
from pricing import VENDED_LOG_SUFFIXES

CONSOLE = "https://console.cloud.google.com"
LOGGING_PRICING_URL = "https://cloud.google.com/stackdriver/pricing"

# Cloud Monitoring's PromQL front end translates a metric type by replacing the
# domain's dots and the first slash; `billing/bytes_ingested` has no labels
# beyond `resource_type` and lives on the `global` monitored resource.
PROMQL_BILLED_BYTES = "logging_googleapis_com:billing_bytes_ingested"
PROMQL_BYTE_COUNT = "logging_googleapis_com:byte_count"

# Resource types with no PromQL schema ("no monitored resource schema found");
# streams on these are proven with a Monitoring API filter instead.
PROMQL_UNSUPPORTED_RESOURCES = frozenset({"vpc_flow_logs_config"})

# Tolerances for the live re-run. Complete invoice months should agree to the
# cent; recent invoice days still receive late rows; metric figures move with
# late-arriving points.
TOL_INVOICE_PCT = 1.0
TOL_INVOICE_RECENT_PCT = 5.0
TOL_SHARE_POINTS = 2.0
TOL_METRIC_PCT = 10.0
TOL_METRIC_TOTAL_PCT = 3.0

# Streams listed per claim in the drawer; the live check still covers all.
MAX_STREAM_SOURCES = 10

_BILLING_ACCOUNT_RE = re.compile(
    r"gcp_billing_export(?:_resource)?_v1_([0-9A-F]{6})_([0-9A-F]{6})_([0-9A-F]{6})",
    re.IGNORECASE,
)

_VENDED_LOGS = ", ".join(sorted(VENDED_LOG_SUFFIXES))

# Drawer prose shared by several claims, stated once.
_SKU_MAPPING = (
    f"Streams bill by log name: {_VENDED_LOGS} as {SKU_LABELS[VENDED]},"
    f" everything else as {SKU_LABELS[LOG_STORAGE]}."
)
_LIST_PRICES = (
    "List prices: committed-use discounts, negotiated rates and credits are"
    " not applied."
)
_LATE_POINTS = "Late-arriving metric points can shift a re-measured value."
_METRIC_LOW = (
    "The metric under-reports on some days (see the notice at the top of the"
    " report)."
)
_PACIFIC_NOTE = (
    "Days and months are Pacific usage dates, as Cloud Billing closes a month;"
    " the invoice view groups by invoice month, which can include late usage"
    " from the month before."
)
_TO_GIB = "÷ 2^30 for GiB"
_METRICS_EXPLORER = "Open Metrics Explorer"


# ==============================================================================
# Small helpers
# ==============================================================================


def _money(v: Optional[float]) -> str:
  return "—" if v is None else f"${v:,.2f}"


def _gib(v: Optional[float]) -> str:
  return "—" if v is None else f"{v:,.2f} GiB"


def _label(sku: str) -> str:
  return SKU_LABELS.get(sku, sku)


def _price_term(gib: float, t: SkuTerms) -> str:
  """One SKU's monthly bill as arithmetic: max(0, GiB − free) × price."""
  if t.free_gib:
    return f"max(0, {gib:,.2f} − {t.free_gib:g}) × ${t.unit_price:g}"
  return f"{gib:,.2f} × ${t.unit_price:g}"


def _utc_days(start: datetime.date, end: datetime.date) -> str:
  """A [start, end) metric window as inclusive UTC days."""
  return f"{start} to {end - datetime.timedelta(days=1)} (UTC)"


def billing_account_from_table(table: Optional[str]) -> Optional[str]:
  """Recovers `XXXXXX-XXXXXX-XXXXXX` from a standard export table name."""
  m = _BILLING_ACCOUNT_RE.search(table or "")
  return "-".join(g.upper() for g in m.groups()) if m else None


def _utc_midnight(d: datetime.date) -> str:
  return f"{d.isoformat()}T00:00:00Z"


def _month_bounds(month: str) -> Tuple[datetime.date, datetime.date]:
  first = datetime.date(int(month[:4]), int(month[5:7]), 1)
  nxt = (first + datetime.timedelta(days=32)).replace(day=1)
  return first, nxt - datetime.timedelta(days=1)


def _source(
    kind: str,
    name: str,
    role: str,
    steps: List[str],
    query: Optional[str] = None,
    language: Optional[str] = None,
    url: Optional[str] = None,
    label: Optional[str] = None,
) -> Dict[str, Any]:
  """One "check it yourself" entry in a claim's drawer."""
  return {
      "name": name,
      "role": role,
      "kind": kind,
      "language": language,
      "query": query,
      "console": {"label": label, "url": url} if url else None,
      "steps": steps,
  }


def _check(
    kind: str, label: str, expect: Dict[str, Any], **fields: Any
) -> Dict[str, Any]:
  """One live re-measurement `verify_claim.py` runs."""
  return {"kind": kind, "label": label, "expect": expect, **fields}


# ==============================================================================
# Console links
# ==============================================================================


def bigquery_url(project: str) -> str:
  # The BigQuery console has no supported parameter that pre-fills a query,
  # so this opens the editor in the right project and the SQL is copied.
  return f"{CONSOLE}/bigquery?project={urllib.parse.quote(project)}"


def billing_reports_url(
    account: Optional[str], project: str, start: str, end: str
) -> Optional[str]:
  """Cloud Billing Reports, filtered to Cloud Logging for one project."""
  if not account:
    return None
  state = ";".join([
      "timeRange=CUSTOM_RANGE",
      f"from={start}",
      f"to={end}",
      f"projects={project}",
      f"products=services%2F{LOGGING_SERVICE_ID}",
      "grouping=GROUP_BY_SKU",
  ])
  return f"{CONSOLE}/billing/{account}/reports;{state}?project={project}"


def metrics_explorer_url(
    project: str, promql: Optional[str] = None, days: int = 0
) -> str:
  """Metrics Explorer, with `promql` pre-filled over `days` days if given."""
  url = f"{CONSOLE}/monitoring/metrics-explorer?project={urllib.parse.quote(project)}"
  if not promql:
    return url
  # `pageState` is the console's own serialisation and is not a documented
  # contract; the PromQL is always offered for copying beside this link.
  state = {
      "xyChart": {
          "dataSets": [{
              "timeSeriesQuery": {
                  "prometheusQuery": promql,
                  "unitOverride": "",
                  "outputFullDuration": False,
              },
              "plotType": "STACKED_BAR",
              "targetAxis": "Y1",
          }],
          "chartOptions": {"mode": "COLOR"},
      },
      "timeSelection": {"timeRange": f"{days}d"},
  }
  return (
      f"{url}&pageState="
      f"{urllib.parse.quote(json.dumps(state, separators=(',', ':')))}"
  )


def logs_explorer_url(project: str, query: str, duration: str = "P14D") -> str:
  return (
      f"{CONSOLE}/logs/query;query={urllib.parse.quote(query, safe='')};"
      f"duration={duration}?project={urllib.parse.quote(project)}"
  )


def log_analytics_url(project: str) -> str:
  return f"{CONSOLE}/logs/analytics?project={urllib.parse.quote(project)}"


def log_router_url(project: str) -> str:
  return f"{CONSOLE}/logs/router?project={urllib.parse.quote(project)}"


# ==============================================================================
# Query text
# ==============================================================================

_CREDITS_SQL = "IFNULL((SELECT SUM(c.amount) FROM UNNEST(credits) c), 0)"
_INGESTION_SQL = f"LOWER(usage.pricing_unit) = '{INGESTION_PRICING_UNIT}'"
_PACIFIC_DAY_SQL = f"DATE(usage_start_time, '{INVOICE_TIMEZONE}')"
_PAYLOAD_SQL = " ".join(PAYLOAD_BYTES_SQL.split())


def _billing_from(
    table: str,
    project_id: str,
    start: datetime.date,
    end: datetime.date,
    ingestion_only: bool = False,
) -> str:
  """FROM/WHERE for one project's Cloud Logging rows on Pacific days."""
  scope = LOGGING_SCOPE_SQL.format(
      service_name=f"'{LOGGING_SERVICE_NAME}'",
      service_id=f"'{LOGGING_SERVICE_ID}'",
      project_id=f"'{project_id}'",
  )
  return (
      f"FROM {quote_table_ref(table)}\nWHERE {scope}\n"
      + (f"  AND {_INGESTION_SQL}\n" if ingestion_only else "")
      + f"  AND {_PACIFIC_DAY_SQL} BETWEEN '{start}' AND '{end}'"
  )


def billing_month_sql(table: str, project_id: str, month: str) -> str:
  """One month's Cloud Logging spend and ingestion, exactly as collected."""
  # The month total (sku = NULL) sorts first, so the live check reads row one.
  first, last = _month_bounds(month)
  return f"""-- Cloud Logging spend for {project_id}, {month} (Pacific usage date).
-- The first row (sku = NULL) is the month total.
SELECT
  sku.description AS sku,
  ROUND(SUM(cost), 2) AS raw_cost,
  ROUND(SUM({_CREDITS_SQL}), 2) AS credits,
  ROUND(SUM(cost + {_CREDITS_SQL}), 2) AS net_cost,
  ROUND(SUM(IF({_INGESTION_SQL}, usage.amount_in_pricing_units, 0)), 2) AS ingested_gib
{_billing_from(table, project_id, first, last)}
GROUP BY ROLLUP(sku)
ORDER BY sku IS NULL DESC, net_cost DESC"""


def billing_unit_price_sql(table: str, project_id: str, month: str) -> str:
  """Per-SKU unit prices, separating free-tier rows from charged ones."""
  first, last = _month_bounds(month)
  return f"""-- What each Cloud Logging SKU actually charges per GiB, {month}
SELECT
  sku.description AS sku,
  ROUND(SUM(usage.amount_in_pricing_units), 2) AS gib,
  ROUND(SUM(IF(cost = 0, usage.amount_in_pricing_units, 0)), 2) AS free_gib,
  ROUND(SAFE_DIVIDE(SUM(IF(cost > 0, cost, 0)),
                    SUM(IF(cost > 0, usage.amount_in_pricing_units, 0))), 4) AS unit_price
{_billing_from(table, project_id, first, last, ingestion_only=True)}
GROUP BY sku
ORDER BY gib DESC"""


def billing_daily_gib_sql(
    table: str, project_id: str, start: datetime.date, end: datetime.date
) -> str:
  return f"""-- Invoiced ingestion per Pacific day, {start} to {end} (complete days only)
SELECT
  COUNT(*) AS days,
  ROUND(SUM(gib), 2) AS total_gib,
  ROUND(AVG(gib), 4) AS avg_daily_gib,
  ROUND(AVG(gib) * {DAYS_PER_MONTH:g}, 2) AS monthly_run_rate_gib
FROM (
  SELECT {_PACIFIC_DAY_SQL} AS d, SUM(usage.amount_in_pricing_units) AS gib
  {_billing_from(table, project_id, start, end, ingestion_only=True)}
  GROUP BY d
)"""


def billing_sku_run_rate_sql(
    table: str, project_id: str, start: datetime.date, end: datetime.date
) -> str:
  """The baseline run rate split by SKU, as the price book splits it."""
  return f"""-- Invoiced ingestion per SKU, Pacific days {start} to {end} (complete days only)
WITH daily AS (
  SELECT sku.description AS sku, {_PACIFIC_DAY_SQL} AS d,
         SUM(usage.amount_in_pricing_units) AS gib
  {_billing_from(table, project_id, start, end, ingestion_only=True)}
  GROUP BY sku, d
)
SELECT
  sku,
  ROUND(SUM(gib), 2) AS total_gib,
  ROUND(SUM(gib) / (SELECT COUNT(DISTINCT d) FROM daily) * {DAYS_PER_MONTH:g}, 2)
    AS monthly_run_rate_gib
FROM daily
GROUP BY sku
ORDER BY total_gib DESC"""


def promql_billed(days: int, by_service: bool = True) -> str:
  """Billed bytes over `days`, per resource type or as one total."""
  inner = (
      f'increase({PROMQL_BILLED_BYTES}{{monitored_resource="global"}}[{days}d])'
  )
  return f"sum by (resource_type) ({inner})" if by_service else f"sum({inner})"


def monitoring_vended_streams_filter() -> str:
  """`byte_count` filter for Vended Logs Storage streams, by log ID suffix."""
  suffixes = "|".join(sorted(VENDED_LOG_SUFFIXES))
  return (
      f'metric.type = "{BYTE_COUNT_METRIC}" AND metric.label.log ='
      f' monitoring.regex.full_match(".*/({suffixes})")'
  )


def promql_stream(
    resource: str, log_id: str, days: int, severity: Optional[str] = None
) -> str:
  sev = f', severity="{severity}"' if severity and severity != "*" else ""
  return (
      f"sum by (log, severity) (increase({PROMQL_BYTE_COUNT}"
      f'{{monitored_resource="{resource}", log="{log_id}"{sev}}}[{days}d]))'
  )


def monitoring_stream_filter(
    log_id: str, severity: Optional[str] = None
) -> str:
  # No `resource.type`: some resources reject it and the collector never used
  # it.
  flt = f'metric.type = "{BYTE_COUNT_METRIC}" AND metric.label.log = "{log_id}"'
  if severity and severity != "*":
    flt += f' AND metric.label.severity = "{severity}"'
  return flt


def severity_share_sql(table: str, start: str, end: str) -> str:
  return f"""-- Share of log content bytes by severity, {start} to {end}
SELECT
  COALESCE(severity, 'DEFAULT') AS severity,
  SUM({_PAYLOAD_SQL}) AS content_bytes,
  ROUND(100 * SUM({_PAYLOAD_SQL})
        / SUM(SUM({_PAYLOAD_SQL})) OVER (), 2) AS share_pct
FROM `{table}`
WHERE timestamp BETWEEN TIMESTAMP('{start}') AND TIMESTAMP('{end}')
GROUP BY severity
ORDER BY content_bytes DESC"""


# ==============================================================================
# Claim builders
# ==============================================================================


class _Ctx:
  """Everything the claim builders share, resolved once."""

  def __init__(self, summary: Dict[str, Any]):
    self.s = summary
    self.project = summary["project_id"]
    now = datetime.datetime.fromisoformat(
        summary["last_updated"].replace("Z", "+00:00")
    )
    self.now = now if now.tzinfo else now.replace(tzinfo=datetime.timezone.utc)
    bm = summary["billing_metadata"]
    self.invoiced = bm["invoiced"]
    self.table = bm["table_name"] and bare_table_ref(bm["table_name"])
    self.billing_project = self.table.split(".")[0] if self.table else None
    self.account = billing_account_from_table(self.table)
    self.cross_project = bool(
        self.billing_project and self.billing_project != self.project
    )
    self.monthly = summary["monthly_aggregations"]
    self.ext = summary["extraneous_spend"]
    self.actions = summary["reduction_actions"]["actions"]
    # Absent when the floor could not be measured.
    self.basis = self.ext.get("basis", {})
    self.window = int(self.basis.get("window_days", DEFAULT_SAMPLE_DAYS))
    self.calibration = self.basis.get("byte_count_to_billed_calibration", 1.0)
    self.t30 = summary["trailing_30d_summary"]
    self.book = PriceBook.from_dict(summary["pricing"])
    self.per_sku = self.book.per_sku
    # A blended book's one rate, free tier spread across its GiB, as the
    # report's tables price it.
    self.rate = round(self.book.average_rate, 4)
    # log_id -> resource types it was seen on, for PromQL's exact-resource rule.
    self.log_resources: Dict[str, List[str]] = {}
    # Present only when the Log Analytics breakdown ran.
    top = summary.get("granular_analytics", {}).get("top_log_names", {})
    for resource, rows in top.items():
      for row in rows:
        lid = row["log_id"]
        if resource not in self.log_resources.setdefault(lid, []):
          self.log_resources[lid].append(resource)
    # No invoice: every volume is the billed-bytes metric and every dollar a
    # list-price estimate, so claims must not borrow the invoiced wording.
    self.telemetry = (
        not self.invoiced
        and self.t30.get("volume_basis") == "cloud_monitoring_metric"
    )

  # --- windows --------------------------------------------------------------

  def utc_window(self, days: int) -> Tuple[datetime.date, datetime.date]:
    """(first day, exclusive end) of a metric window, in UTC days."""
    # The collector floors to UTC midnight, so today is excluded.
    end = self.now.astimezone(datetime.timezone.utc).date()
    return end - datetime.timedelta(days=days), end

  @property
  def invoice_window(self) -> Tuple[datetime.date, datetime.date]:
    """The trailing run-rate window over complete invoice days."""
    start = (
        self.now - datetime.timedelta(days=DEFAULT_TELEMETRY_LOOKBACK_DAYS)
    ).date()
    return start, last_complete_invoice_day(self.now)

  # --- wording that depends on where the numbers came from -----------------

  @property
  def volume_basis(self) -> str:
    """Where the monthly baseline volume came from, for formula text."""
    days = DEFAULT_TELEMETRY_LOOKBACK_DAYS
    if self.invoiced:
      return f"trailing {days} days of invoiced ingestion"
    return f"trailing {days} days of {BILLED_BYTES_METRIC}; no billing export"

  @property
  def priced_against(self) -> str:
    if self.invoiced:
      return " invoiced baseline."
    return " estimated baseline at list price (no billing export)."

  # --- per-SKU pricing, shared by every dollar claim ------------------------

  def _split_basis(self) -> str:
    check = self.book.mapping_check
    if check.get("split_source") == "billing_export":
      return "split by the SKU the invoice billed it under"
    share = check.get("telemetry_vended_share_pct")
    return f"split by SKU in proportion to byte_count on the {_VENDED_LOGS}" + (
        f" streams ({share}% of measured volume)" if share is not None else ""
    )

  def baseline_formula(self) -> List[str]:
    """The per-SKU baseline bill, as arithmetic with the real inputs."""
    book = self.book
    skus = book.skus.items()
    list_priced = all(t.price_source == "list" for t in book.skus.values())
    return [
        f"Baseline: {_gib(book.baseline_gib)}/month ({self.volume_basis}),"
        f" {self._split_basis()}: "
        + ", ".join(f"{_label(k)} {_gib(t.baseline_gib)}" for k, t in skus)
        + ".",
        "  Bill = "
        + " + ".join(_price_term(t.baseline_gib, t) for _, t in skus)
        + f" = {_money(book.baseline_cost)}/month"
        + (" at list prices." if list_priced else "."),
    ]

  def saving_formula(
      self, gib_by_sku: Dict[str, float], usd: Optional[float]
  ) -> List[str]:
    """One line per SKU showing how a saving was priced."""
    lines = [f"Saving {_money(usd)}/mo = the sum over the SKUs it removes:"]
    for sku, gib in sorted(gib_by_sku.items()):
      if not gib:
        continue
      t = self.book.terms(sku)
      part = _money(self.book.saving({sku: gib}))
      base = _gib(t.baseline_gib)
      if t.free_gib:
        lines.append(
            f"  • {_label(sku)}: (billable({base}) − billable({base} −"
            f" {_gib(gib)})) × ${t.unit_price:g}/GiB = {part}, billable(x) ="
            f" max(0, x − {t.free_gib:g} GiB)."
        )
      else:
        lines.append(
            f"  • {_label(sku)}: {_gib(gib)} × ${t.unit_price:g}/GiB = {part}."
        )
    return lines

  def pricing_sources(self) -> List[Dict[str, Any]]:
    """The sources that reproduce the unit prices behind a dollar figure."""
    if not self.invoiced:
      if not self.telemetry:
        return []
      return [
          _source(
              "pricing",
              "Cloud Logging list prices",
              "The unit prices and free tier behind every dollar figure",
              [f"Prices applied: {self.book.formula_terms()}."],
              url=LOGGING_PRICING_URL,
              label="Open the pricing page",
          )
      ]
    if not self.per_sku:
      return []
    start, end = self.invoice_window
    sources = [
        self.billing_source(
            "Baseline split by SKU",
            billing_sku_run_rate_sql(self.table, self.project, start, end),
            "How much of the monthly volume each SKU bills",
        )
    ]
    for month in sorted(
        {t.price_month for t in self.book.skus.values() if t.price_month}
    ):
      sources.append(
          self.billing_source(
              f"Per-SKU unit prices, {month}",
              billing_unit_price_sql(self.table, self.project, month),
              "What each SKU charged per GiB, free-tier rows separated",
          )
      )
    return sources

  def rate_desc(self) -> str:
    """The rate behind a table's estimated dollars, to follow "GiB × "."""
    if not self.per_sku:
      kind = "the invoiced blended rate" if self.invoiced else "list price"
      return f"${self.rate}/GiB ({kind})."
    rates = ", ".join(
        f"{_label(k)} ${t.effective_rate:.4f}/GiB"
        for k, t in sorted(self.book.skus.items())
    )
    return (
        f"its SKU's effective rate: {rates} (monthly bill ÷ monthly GiB, so"
        " the free tier is spread across the SKU's GiB)."
    )

  def pricing_differences(self) -> List[str]:
    """Why a priced figure may differ from the console, per pricing mode."""
    if not self.per_sku:
      return self.book.notes or [
          "One blended rate across SKUs; Vended Logs Storage streams (e.g. VPC"
          " flow logs) bill at a lower unit price than it assumes."
      ]
    check = self.book.mapping_check
    gap = check.get("gap_points")
    if gap is not None:
      return [
          f"{_SKU_MAPPING} That puts"
          f" {check.get('telemetry_vended_share_pct')}% of measured volume on"
          f" Vended against {check.get('invoice_vended_share_pct')}% on the"
          f" invoice ({gap} points apart)."
      ]
    if not self.invoiced:
      return [
          (
              f"{_SKU_MAPPING} With no billing export, no invoice checks that"
              " split."
          ),
          _LIST_PRICES,
      ]
    return [_SKU_MAPPING]

  # --- sources --------------------------------------------------------------

  def billing_source(self, name: str, sql: str, role: str) -> Dict[str, Any]:
    steps = [
        f"Open BigQuery in project `{self.billing_project}` and paste the SQL."
    ]
    if self.cross_project:
      steps.append(
          f"The export lives in `{self.billing_project}`, not"
          f" `{self.project}`: you need BigQuery Data Viewer on that dataset"
          " and Job User in some project."
      )
    return _source(
        "billing_export",
        name,
        role,
        steps,
        query=sql,
        language="sql",
        url=bigquery_url(self.billing_project or self.project),
        label="Open BigQuery",
    )

  def reports_source(self, month: str) -> Optional[Dict[str, Any]]:
    first, last = _month_bounds(month)
    url = billing_reports_url(
        self.account, self.project, first.isoformat(), last.isoformat()
    )
    if not url:
      return None
    return _source(
        "billing_reports",
        f"Cloud Billing Reports, {month}",
        "Independent cross-check in the console",
        [
            "Pre-filtered to Cloud Logging, this project and the month, by"
            " SKU. Include 'Promotions and others' credits to match the net."
        ],
        url=url,
        label="Open Billing Reports",
    )

  def promql_source(
      self, name: str, promql: str, days: int, role: str, eval_note: str
  ) -> Dict[str, Any]:
    return _source(
        "cloud_monitoring",
        name,
        role,
        ["Metrics Explorer → Code → PromQL, paste the query, Run.", eval_note],
        query=promql,
        language="promql",
        url=metrics_explorer_url(self.project, promql, days),
        label=_METRICS_EXPLORER,
    )

  def daily_bars_source(
      self, name: str, days: int, role: str, step: str
  ) -> Dict[str, Any]:
    """The billed-bytes metric as one stacked bar per day."""
    return self.promql_source(
        name, promql_billed(1), days, role, f"Stacked bars, 1-day step; {step}"
    )

  def telemetry_volume_source(self, role: str) -> Dict[str, Any]:
    """The PromQL that reproduces the trailing 30-day billed total."""
    days = DEFAULT_TELEMETRY_LOOKBACK_DAYS
    start, end = self.utc_window(days)
    return self.promql_source(
        f"Billed bytes, {_utc_days(start, end)}",
        promql_billed(days, by_service=False),
        days,
        role,
        f"Evaluate at {_utc_midnight(end)} so the window is exactly the whole"
        f" UTC days summed. Result is bytes; {_TO_GIB}.",
    )

  def baseline_source(self, name: str, role: str) -> Optional[Dict[str, Any]]:
    """The monthly volume every percentage and saving is taken from."""
    if self.invoiced:
      start, end = self.invoice_window
      return self.billing_source(
          name,
          billing_daily_gib_sql(self.table, self.project, start, end),
          role,
      )
    if self.telemetry:
      return self.telemetry_volume_source(role)
    return None

  def run_rate_check(self, label: str) -> Optional[Dict[str, Any]]:
    """Live check of the monthly run-rate GiB, re-read from its source."""
    run_rate = self.t30.get("monthly_run_rate_gib")
    if run_rate is None:
      return None
    if self.invoiced:
      start, end = self.invoice_window
      return _check(
          "bigquery",
          label,
          {"monthly_run_rate_gib": run_rate},
          project=self.billing_project,
          query=billing_daily_gib_sql(self.table, self.project, start, end),
          tolerance_pct=TOL_INVOICE_RECENT_PCT,
      )
    days_seen = self.t30.get("days_observed")
    if not self.telemetry or not days_seen:
      return None
    days = DEFAULT_TELEMETRY_LOOKBACK_DAYS
    return _check(
        "promql",
        label,
        {"total": run_rate},
        query=promql_billed(days, False),
        time=_utc_midnight(self.utc_window(days)[1]),
        compare="total",
        scale=DAYS_PER_MONTH / days_seen / BYTES_PER_GIB,
        unit="GiB/month",
        tolerance_pct=TOL_METRIC_TOTAL_PCT,
    )

  def stream_sources_and_checks(
      self,
      claims: Sequence[Dict[str, Any]],
      expect_gib: float,
      fraction: float = 1.0,
  ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Sources for the largest streams behind an action, and one live check.

    Args:
      claims: The action's per-stream claims.
      expect_gib: The monthly GiB the check should re-measure.
      fraction: Share of each stream the action claims (e.g. the bytes a lower
        flow-log sampling rate would drop). 1.0 for whole-stream actions.

    Returns:
      (sources, checks). The check covers every stream; the drawer lists the
      `MAX_STREAM_SOURCES` largest.
    """
    role = "Claimed stream volume"
    window, cal = self.window, self.calibration
    start, end = self.utc_window(window)
    scale = (
        f"× {cal:g} (calibration)"
        + (f" × {fraction:g} (claimed share)" if fraction != 1.0 else "")
        + f" × {DAYS_PER_MONTH:g}/{window} {_TO_GIB}/month."
    )
    streams = sorted(
        (c for c in claims if c.get("log_id")),
        key=lambda c: -(c.get("monthly_gib") or 0.0),
    )
    sources: List[Dict[str, Any]] = []
    for claim in streams[:MAX_STREAM_SOURCES]:
      lid = claim["log_id"]
      sev = claim.get("severity") or "*"
      sev_label = f" ({sev})" if sev != "*" else ""
      resources = self.log_resources.get(lid) or []
      if resources and not PROMQL_UNSUPPORTED_RESOURCES.intersection(resources):
        sources += [
            self.promql_source(
                f"{lid} on {resource}{sev_label}",
                promql_stream(resource, lid, window, sev),
                window,
                role,
                f"Evaluate at {_utc_midnight(end)}. Bytes over {window} days;"
                f" {scale}",
            )
            for resource in resources
        ]
        continue
      # PromQL needs an exact resource; the Monitoring filter does not.
      sources.append(
          _source(
              "cloud_monitoring",
              f"{lid}{sev_label}",
              role,
              [
                  (
                      f"Metric = {BYTE_COUNT_METRIC}, this filter, Aggregation"
                      f" = Sum, Alignment = 1 day, {_utc_days(start, end)}."
                  ),
                  f"Sum the daily bars, then {scale}",
              ],
              query=monitoring_stream_filter(lid, sev),
              language="monitoring_filter",
              url=metrics_explorer_url(self.project),
              label=_METRICS_EXPLORER,
          )
      )
    hidden = len(streams) - MAX_STREAM_SOURCES
    if hidden > 0:
      sources.append(
          _source(
              "cloud_monitoring",
              f"…and {hidden} smaller streams",
              role,
              [f"verify_claim.py re-measures all {len(streams)} streams."],
          )
      )
    if not streams:
      return sources, []
    series = [
        {
            "filter": monitoring_stream_filter(c["log_id"], c.get("severity")),
            "log_id": c["log_id"],
        }
        for c in streams
    ]
    return sources, [
        _check(
            "monitoring_sum",
            "Re-measure the claimed streams (Monitoring API)",
            {"total": expect_gib},
            series=series,
            start=_utc_midnight(start),
            end=_utc_midnight(end),
            multiplier=cal * fraction * DAYS_PER_MONTH / window / BYTES_PER_GIB,
            unit="GiB/month",
            tolerance_pct=TOL_METRIC_PCT,
        )
    ]

  def metric_differences(self) -> List[str]:
    """Why a metric-derived figure may differ from a console reading."""
    diffs = [
        (
            "No billing export: this is Cloud Monitoring's"
            f" {BILLED_BYTES_METRIC}, not an invoice. Healthy, it reads a few"
            " percent above the invoice; on some days it reads far below with"
            " no gap to signal it."
        ),
        (
            "Whole UTC days; today is excluded. PromQL increase() extrapolates"
            " slightly at the window edges."
        ),
    ]
    days_seen = self.t30.get("days_observed")
    lookback = DEFAULT_TELEMETRY_LOOKBACK_DAYS
    if days_seen and days_seen < lookback:
      diffs.append(
          f"Only {days_seen} of {lookback} days had data, so the daily average"
          f" divides by {days_seen}."
      )
    return diffs


def _claim(
    cid: str,
    title: str,
    value: str,
    summary_line: str,
    formula: List[str],
    sources: Sequence[Optional[Dict[str, Any]]],
    differences: List[str],
    checks: Sequence[Optional[Dict[str, Any]]],
    see_also: Sequence[str] = (),
) -> Dict[str, Any]:
  return {
      "id": cid,
      "title": title,
      "value": value,
      "summary": summary_line,
      "formula": formula,
      "sources": [s for s in sources if s],
      "differences": differences,
      "checks": [c for c in checks if c],
      # Claims this one is built from; each proves its own inputs.
      "see_also": list(see_also),
  }


def _invoice_check(
    c: _Ctx, label: str, month: str, expect: Dict[str, Any], tol: float
) -> Dict[str, Any]:
  return _check(
      "bigquery",
      label,
      expect,
      project=c.billing_project,
      query=billing_month_sql(c.table, c.project, month),
      tolerance_pct=tol,
  )


def _latest_invoiced_month(c: _Ctx) -> Optional[Dict[str, Any]]:
  """The latest complete month, if the invoice covers it."""
  # A month estimated from telemetry before the export began has no invoice to
  # prove it against.
  month = c.s["latest_complete_month"]
  if not c.invoiced or not month:
    return None
  m = c.monthly[month]
  return m if m["data_source"] == "actual_bq_billing" else None


def _latest_complete_spend(c: _Ctx) -> Optional[Dict[str, Any]]:
  """Proves the last complete invoice month's net Cloud Logging spend."""
  m = _latest_invoiced_month(c)
  if not m:
    return None
  month = c.s["latest_complete_month"]
  sql = billing_month_sql(c.table, c.project, month)
  return _claim(
      "latest_complete_spend",
      "Latest Complete Spend",
      f"{_money(m['net_cost_usd'])} · {month}",
      "Read directly from your Cloud Billing export; no estimate.",
      [
          (
              f"{_money(m['net_cost_usd'])} = Σ (cost + credits) over every"
              f" Cloud Logging SKU for {c.project}, {month}"
          ),
          (
              f"  = {_money(m['raw_cost_usd'])} cost +"
              f" {_money(m['credits_usd'])} credits:"
          ),
          *(
              f"  • {k}: {_money(v)}"
              for k, v in sorted(m["cost_by_sku"].items())
          ),
          (
              f"{_gib(m['total_gib'])} = Σ usage in '{INGESTION_PRICING_UNIT}'"
              " (ingestion only; retention bills in GiB-months)."
          ),
      ],
      [
          c.billing_source(
              f"Billing export, {month}", sql, "Every dollar and GiB here"
          ),
          c.reports_source(month),
      ],
      [
          _PACIFIC_NOTE,
          (
              "Dollars cover every Cloud Logging SKU, retention included; GiB"
              " is ingestion only, so dollars ÷ GiB is not a unit price."
          ),
          "The export can receive corrections for a few days after month end.",
      ],
      [
          _invoice_check(
              c,
              f"Re-run the {month} billing query",
              month,
              {"net_cost": m["net_cost_usd"], "ingested_gib": m["total_gib"]},
              TOL_INVOICE_PCT,
          )
      ],
  )


def _mtd_run_rate(c: _Ctx) -> Optional[Dict[str, Any]]:
  """Proves month-to-date spend and the straight-line month-end projection."""
  proj = c.s["cost_projection"]
  month = proj["month"]
  # On the 1st the export may have no rows for the projected month yet; never
  # pair last month's spend with this month's projection.
  if not c.invoiced or month not in c.monthly:
    return None
  m = c.monthly[month]
  first, last = _month_bounds(month)
  complete_end = min(last_complete_invoice_day(c.now), last)
  eom = sorted(proj["projected_eom_gib_by_sku"].items())
  formula = [
      f"Month to date: {_money(m['net_cost_usd'])} = Σ (cost + credits),"
      f" {first} to today (Pacific), all Cloud Logging SKUs."
  ]
  if eom:
    formula += [
        f"Projected month end: {_money(proj['projected_eom_cost_usd'])} = "
        + " + ".join(_price_term(g, c.book.terms(k)) for k, g in eom)
        + " ("
        + ", ".join(f"{_label(k)} {_gib(g)}" for k, g in eom)
        + ").",
        (
            "  Each SKU's month-end GiB = its mean invoiced GiB/day over"
            f" complete days {first} to {complete_end} × {last.day} days."
        ),
    ]
  return _claim(
      "mtd_run_rate",
      "Current MTD Run-Rate",
      f"{_money(m['net_cost_usd'])} MTD · projected"
      f" {_money(proj['projected_eom_cost_usd'])}",
      "Month-to-date spend is invoiced; month end is a straight-line"
      " projection of invoiced daily volume.",
      formula,
      [
          c.billing_source(
              f"Billing export, {month} to date",
              billing_month_sql(c.table, c.project, month),
              "Month-to-date spend and GiB",
          ),
          c.billing_source(
              "Daily invoiced GiB behind the projection",
              billing_daily_gib_sql(c.table, c.project, first, complete_end),
              "Mean GiB/day",
          ),
          c.billing_source(
              "Per-SKU unit prices",
              billing_unit_price_sql(c.table, c.project, month),
              "What each SKU charges per GiB",
          ),
          c.reports_source(month),
      ],
      [
          _PACIFIC_NOTE,
          "The export lags up to a day, so today's spend grows between runs.",
          (
              "The projection holds each SKU at its month-to-date daily"
              " average; the free tier applies once, to the whole month."
          ),
      ],
      [
          _invoice_check(
              c,
              f"Re-run the {month} month-to-date query",
              month,
              {"net_cost": m["net_cost_usd"]},
              TOL_INVOICE_RECENT_PCT,
          )
      ],
  )


def _invoiced_driver_cost(m: Dict[str, Any], name: str, month: str) -> str:
  """How the invoice's ingestion dollars were apportioned to one service."""
  details, top = m["services_details"], m["services_details"][name]
  if m["services_cost_basis"] != "per_sku":
    return (
        f"{_money(top['cost_usd'])} = {top['pct_of_volume']}% ×"
        f" {_money(m['ingestion_cost_usd'])} invoiced ingestion cost,"
        " apportioned to the cent."
    )
  sku = sku_of_resource(name)
  pool = [v["bytes"] for k, v in details.items() if sku_of_resource(k) == sku]
  sku_cost = (m["ingestion_by_sku"].get(sku) or {}).get("net_cost_usd")
  return (
      f"{_money(top['cost_usd'])} = {top['bytes'] / (sum(pool) or 1):.1%} of"
      f" the bytes of the {len(pool)} services billed as {_label(sku)} ×"
      f" {_money(sku_cost)} {_label(sku)} cost for {month}, apportioned to the"
      " cent. Each SKU's cost is split only across the services it bills."
  )


def _top_cost_driver(c: _Ctx) -> Optional[Dict[str, Any]]:
  """Proves the top service's share of volume and its dollars."""
  if c.invoiced:
    m = _latest_invoiced_month(c)
    name = m and m["top_service"]
    if not name:
      return None
    month = c.s["latest_complete_month"]
    top = m["services_details"][name]
    share, cost = top["pct_of_volume"], top["cost_usd"]
    _, last = _month_bounds(month)
    days = max(m["services_telemetry_days"], 1)
    start = last - datetime.timedelta(days=days - 1)
    end = last + datetime.timedelta(days=1)
    summary = (
        "The share is from Cloud Monitoring; the GiB and dollars it applies to"
        " are from your invoice."
    )
    formula = [
        (
            f"{_gib(top['billed_gib'])} = {share}% × {_gib(m['total_gib'])}"
            " invoiced ingestion."
        ),
        _invoiced_driver_cost(m, name, month),
    ]
    sources = [
        c.billing_source(
            f"Billing export, {month}",
            billing_month_sql(c.table, c.project, month),
            "The invoiced GiB and dollars the share is applied to",
        )
    ]
    differences = [
        "Monitoring days are UTC; invoice days are Pacific.",
        f"{_METRIC_LOW} Shares on those days are indicative.",
    ]
    if days < last.day:
      differences.insert(
          0,
          f"Only {days} of {last.day} days of {month} are within Cloud"
          f" Monitoring's {MONITORING_RETENTION_DAYS}-day retention; the share"
          " assumes the rest of the month had the same mix.",
      )
  elif c.telemetry and c.t30.get("top_driver"):
    name = c.t30["top_driver"]
    top = next(s for s in c.t30["top_services"] if s["service"] == name)
    share, cost = top["pct_of_total"], top["cost_usd"]
    days = DEFAULT_TELEMETRY_LOOKBACK_DAYS
    start, end = c.utc_window(days)
    total = c.t30["total_gib"]
    monthly_gib = (
        top["gib"] * c.t30["monthly_run_rate_gib"] / total if total else 0
    )
    sku = c.book.sku_for_resource(name)
    summary = (
        "Share and volume from Cloud Monitoring's billed-bytes metric, priced"
        " at list. No billing export was used."
    )
    formula = [
        (
            f"{_gib(top['gib'])} = {share}% × {_gib(total)} trailing {days}-day"
            " volume."
        ),
        (
            f"{_money(cost)}/mo = {_gib(monthly_gib)}/month ×"
            f" ${c.book.terms(sku).effective_rate:.4f}/GiB, the effective"
            f" {_label(sku)} rate (its monthly bill ÷ its monthly GiB)."
        ),
        "Ranked by estimated dollars, then volume.",
    ]
    sources = c.pricing_sources()
    differences = c.metric_differences() + c.pricing_differences()
  else:
    return None
  promql = promql_billed(days)
  return _claim(
      "top_cost_driver",
      "Top Cost Driver",
      f"{name} · {share}% · {_money(cost)}",
      summary,
      [
          f"Share {share}% = {name} bytes ÷ all bytes in"
          f" {BILLED_BYTES_METRIC}, {_utc_days(start, end)}."
      ]
      + formula,
      [
          c.promql_source(
              f"Service mix, {_utc_days(start, end)}",
              promql,
              days,
              "The share",
              f"Evaluate at {_utc_midnight(end)} (or Table view on a custom"
              f" range); divide the {name} row by the sum of all rows.",
          )
      ]
      + sources,
      differences,
      [
          _check(
              "promql",
              f"Re-measure {name}'s share",
              {name: share},
              query=promql,
              time=_utc_midnight(end),
              compare="share",
              label_key="resource_type",
              tolerance_points=TOL_SHARE_POINTS,
          )
      ],
  )


# ------------------------------------------------------------------------------
# Telemetry-mode KPI claims (no billing export): metric volumes, list prices.
# ------------------------------------------------------------------------------


def _trailing_30d_volume(c: _Ctx) -> Optional[Dict[str, Any]]:
  """Proves the Trailing 30-Day Volume card shown without an invoice."""
  days_seen = c.t30.get("days_observed")
  if not c.telemetry or not days_seen:
    return None
  total, daily = c.t30["total_gib"], c.t30["daily_avg_gib"]
  days = DEFAULT_TELEMETRY_LOOKBACK_DAYS
  start, end = c.utc_window(days)
  return _claim(
      "trailing_30d_volume",
      "Trailing 30-Day Volume",
      f"{_gib(total)} · {_gib(daily)}/day",
      "Summed from Cloud Monitoring's billed-bytes metric: metered volume,"
      " not invoiced (no billing export).",
      [
          (
              f"{_gib(total)} = Σ {BILLED_BYTES_METRIC} bytes across every"
              f" resource type, {_utc_days(start, end)}, {_TO_GIB}."
          ),
          (
              f"Daily average {_gib(daily)}/day = {total:,.2f} GiB ÷"
              f" {days_seen} day{'s' if days_seen != 1 else ''} with data."
          ),
      ],
      [
          c.telemetry_volume_source("Every GiB in this figure"),
          c.daily_bars_source(
              "Same metric, one bar per day",
              days,
              "The daily series behind the average",
              f"sum the bars over {_utc_days(start, end)}.",
          ),
      ],
      c.metric_differences(),
      [
          _check(
              "promql",
              "Re-measure trailing 30-day volume",
              {"total": total},
              query=promql_billed(days, False),
              time=_utc_midnight(end),
              compare="total",
              scale=1 / BYTES_PER_GIB,
              unit="GiB",
              tolerance_pct=TOL_METRIC_TOTAL_PCT,
          )
      ],
  )


def _estimated_run_rate(c: _Ctx) -> Optional[Dict[str, Any]]:
  """Proves the Estimated Monthly Run-Rate card shown without an invoice."""
  if not c.telemetry or not c.t30.get("days_observed"):
    return None
  run_rate = c.t30["monthly_run_rate_gib"]
  cost = c.t30["projected_monthly_cost_usd"]
  annual = c.t30["projected_annual_cost_usd"]
  formula = [
      (
          f"Run rate {_gib(run_rate)}/month ="
          f" {_gib(c.t30['daily_avg_gib'])}/day × {DAYS_PER_MONTH:g} days."
      ),
      *c.baseline_formula(),
      f"Annualized {_money(annual)} = {_money(cost)} × 12.",
  ]
  sources: List[Optional[Dict[str, Any]]] = [
      c.telemetry_volume_source("The volume behind the run rate")
  ]
  check = c.book.mapping_check
  if c.per_sku and check.get("split_source") == "cloud_monitoring_byte_count":
    sources.append(
        _source(
            "cloud_monitoring",
            "Vended network log streams (byte_count)",
            "How the run rate splits between the two SKUs",
            [
                (
                    f"Metric = {BYTE_COUNT_METRIC}, Aggregation = Sum,"
                    " Alignment = 1 day, over the stream window. Vended share"
                    " = total with this filter ÷ total without it"
                    f" ({check.get('telemetry_vended_share_pct')}% in the"
                    " report)."
                ),
                (
                    "On a large project read the unfiltered total a few days at"
                    " a time; one read over the whole window can time out."
                ),
            ],
            query=monitoring_vended_streams_filter(),
            language="monitoring_filter",
            url=metrics_explorer_url(c.project),
            label=_METRICS_EXPLORER,
        )
    )
  return _claim(
      "estimated_run_rate",
      "Estimated Monthly Run-Rate",
      f"{_money(cost)}/mo · {_money(annual)}/yr",
      "Trailing 30-day metered volume projected to a month and priced at"
      " Cloud Logging list prices (no billing export).",
      formula,
      sources + c.pricing_sources(),
      c.metric_differences()
      + [
          "Ingestion only; retention past the included 30 days bills"
          " separately."
      ]
      + c.pricing_differences(),
      [c.run_rate_check("Re-measure the monthly run-rate volume")],
  )


# ------------------------------------------------------------------------------
# Savings and breakdowns.
# ------------------------------------------------------------------------------


def _calibration_line(b: Dict[str, Any], cal: float, window: int) -> str:
  """The byte_count → billed calibration, as arithmetic that adds up."""
  anchor, received = b["anchor_window_gib"], b["byte_count_window_gib"]
  anchor_label = (
      "invoiced"
      if b["calibration_anchor"] == "billing_export"
      else f"billed ({BILLED_BYTES_METRIC})"
  )
  sides = (
      f"{_gib(anchor)} {anchor_label} ÷ {_gib(received)} received (byte_count)"
      f" over {window} days"
  )
  raw = anchor / received if anchor and received else None
  if raw is not None and raw > cal + 0.005:
    # Calibration is capped at 1: scaling stream bytes up would invent savings.
    return (
        f"Calibration ×{cal:g}: {sides} = ×{raw:.2f}, capped at ×1. Billed"
        " exceeds received (e.g. entries routed to several buckets), so stream"
        " bytes are used as measured and every action stays a floor."
    )
  return f"Calibration ×{cal:g} = {sides}; stream volumes scale onto billed."


def _extraneous_spend(c: _Ctx) -> Optional[Dict[str, Any]]:
  """Proves the extraneous-spend floor; each counted action proves itself."""
  if c.ext.get("status") != "ok":
    return None
  hl, b, window = c.ext["headline"], c.basis, c.window
  levers = [a for a in c.actions if a["counted"]]
  rule = (
      "Each counted action: GiB/month = claimed stream bytes × calibration ×"
      f" {DAYS_PER_MONTH:g}/{window}"
  )
  if c.per_sku:
    formula = c.baseline_formula() + [
        _calibration_line(b, c.calibration, window),
        (
            f"{rule}, priced on the SKU each stream bills under; % = saving ÷"
            f" {_money(c.book.baseline_cost)} baseline bill."
        ),
    ]
  else:
    t = c.book.terms(BLENDED)
    formula = [
        (
            f"Baseline: {_gib(b['baseline_monthly_gib'])}/month"
            f" ({c.volume_basis}) − {t.free_gib:g} GiB free ="
            f" {_gib(b['billable_monthly_gib'])} billable ×"
            f" ${t.unit_price:g}/GiB = {_money(c.book.baseline_cost)}/month."
        ),
        _calibration_line(b, c.calibration, window),
        (
            f"{rule}; saving = billable(baseline) − billable(baseline − action"
            " GiB), × rate."
        ),
    ]
  for lv in levers:
    split = ", ".join(
        f"{_gib(g)} {_label(k)}" for k, g in sorted(lv["gib_by_sku"].items())
    )
    formula.append(
        f"  • {lv['title']}: {_gib(lv['monthly_gib'])}/mo"
        + (f" ({split})" if split and c.per_sku else "")
        + f" → {_money(lv['monthly_usd'])}/mo ({lv['pct_of_billable']}%)"
    )
  formula.append(
      f"Floor = Σ counted actions = ≥ {hl['pct_of_billable_spend']}%"
      f" ({_money(hl['monthly_savings_usd'])}/mo). Uncounted actions are never"
      " added. Each action's own Prove It lists and re-measures its streams."
  )
  return _claim(
      "extraneous_spend",
      "Extraneous Log Spend",
      f"≥ {hl['pct_of_billable_spend']}% ·"
      f" {_money(hl['monthly_savings_usd'])}/mo",
      "A floor: only actions measured from Cloud Monitoring volume metrics"
      " count, each against an"
      + c.priced_against,
      formula,
      [
          c.baseline_source(
              f"Baseline: {c.volume_basis}", "Denominator of every percentage"
          ),
          *c.pricing_sources(),
      ],
      [
          "Each action is priced alone against the full baseline, so the sum"
          " is not a joint saving where the free tier matters."
      ]
      + c.pricing_differences(),
      [c.run_rate_check("Re-measure the baseline")],
      see_also=[f"action::{lv['id']}" for lv in levers],
  )


def _shared_window(summary: Dict[str, Any]) -> List[str]:
  daily = summary["daily_services"]
  dates = sorted(d for d, v in daily.items() if sum(v.values()) > 0)
  return dates[-DEFAULT_SAMPLE_DAYS:]


def _service_mix(c: _Ctx) -> Optional[Dict[str, Any]]:
  """Proves the By Service table's daily GiB and estimated dollars."""
  dates = _shared_window(c.s)
  if not dates:
    return None
  totals: Dict[str, float] = {}
  for d in dates:
    for svc, b in c.s["daily_services"][d].items():
      totals[svc] = totals.get(svc, 0.0) + b
  grand = sum(totals.values()) or 1.0
  top = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)[:5]
  start = datetime.date.fromisoformat(dates[0])
  end = datetime.date.fromisoformat(dates[-1]) + datetime.timedelta(days=1)
  window = _utc_days(start, end)
  promql = promql_billed(len(dates))
  return _claim(
      "service_mix",
      "Service mix",
      f"{len(dates)}-day breakdown by service",
      "Straight from Cloud Monitoring's billed-bytes metric, one of the"
      " metrics Google bills from.",
      [
          (
              f"GiB per service = Σ {BILLED_BYTES_METRIC} bytes by"
              f" resource_type, {window}, {_TO_GIB}."
          ),
          f"Est. cost = service GiB × {c.rate_desc()}",
          *(
              f"  • {svc}: {_gib(b / BYTES_PER_GIB)} ({b / grand * 100:.1f}%)"
              for svc, b in top
          ),
      ],
      [
          c.promql_source(
              f"Billed bytes by service, {window}",
              promql,
              len(dates),
              "Every row in the table",
              f"Evaluate at {_utc_midnight(end)}; Table view gives one total"
              " per service.",
          ),
          c.daily_bars_source(
              "Same metric, one bar per day",
              len(dates),
              "The daily chart",
              "one bar per service per day.",
          ),
      ],
      [
          (
              "Dollars are GiB × rate with no credits, so the table will not"
              " equal invoiced dollars for the same days."
          ),
          f"Raw metric bytes, not rescaled to the invoice. {_METRIC_LOW}",
      ],
      [
          _check(
              "promql",
              "Re-measure service GiB",
              {svc: round(b / BYTES_PER_GIB, 2) for svc, b in top},
              query=promql,
              time=_utc_midnight(end),
              compare="value",
              scale=1 / BYTES_PER_GIB,
              label_key="resource_type",
              tolerance_pct=TOL_METRIC_TOTAL_PCT,
          )
      ],
  )


def _severity_costs(c: _Ctx) -> Optional[Dict[str, Any]]:
  """Proves the By Severity table's shares, GiB and estimated dollars."""
  sev = c.s["severity_summary"]
  totals = sev["severity_totals"]
  if not totals:
    return None
  grand = sum(totals.values()) or 1.0
  shares = {k: round(v / grand * 100, 2) for k, v in totals.items()}
  ga = c.s.get("granular_analytics") or {}
  start, end = ga.get("sample_start"), ga.get("sample_end")
  if c.per_sku:
    cost_line = (
        "Est. cost = severity share × the day's dollars, each service's GiB"
        f" priced at {c.rate_desc()}"
    )
  else:
    cost_line = f"Est. cost = severity GiB × ${c.rate}/GiB."
  formula = [
      (
          "Per day: severity GiB = that severity's share of log content bytes ×"
          f" the day's billed GiB ({BILLED_BYTES_METRIC})."
      ),
      cost_line,
      "Window shares:",
      *(
          f"  • {k}: {v}%"
          for k, v in sorted(shares.items(), key=lambda kv: -kv[1])
      ),
  ]
  sources: List[Optional[Dict[str, Any]]] = []
  checks: List[Optional[Dict[str, Any]]] = []
  table = c.s["analytics_metadata"]["table_name"]
  if sev.get("severity_source") == "log_analytics" and start and end and table:
    sql = severity_share_sql(table, start, end)
    sources.append(
        _source(
            "log_analytics",
            "Severity weights (Log Analytics)",
            "The share of each severity",
            [
                "Observability Analytics → paste the SQL → Run. It also runs"
                " as is in BigQuery, where the collector ran it."
            ],
            query=sql,
            language="sql",
            url=log_analytics_url(c.project),
            label="Open Observability Analytics",
        )
    )
    checks.append(
        _check(
            "bigquery",
            "Re-run the severity share query",
            shares,
            project=c.project,
            query=sql,
            compare="share_rows",
            row_key="severity",
            row_value="share_pct",
            tolerance_points=TOL_SHARE_POINTS,
        )
    )
  return _claim(
      "severity_costs",
      "Severity costs",
      "Breakdown by severity",
      "Severity shares come from your log contents; the daily volume they"
      " split is the service mix's billed-bytes metric.",
      formula,
      sources,
      [
          (
              "Content bytes exclude labels and metadata, so large payloads"
              " weigh more."
          ),
          "Log Analytics buckets by event time, the metric by ingestion time.",
          "As in the service table: no credits, free tier spread per SKU.",
      ],
      checks,
      see_also=["service_mix"] if _shared_window(c.s) else [],
  )


def _action(c: _Ctx, action: Dict[str, Any]) -> Optional[Dict[str, Any]]:
  """Proves one cost optimization action's volume and saving."""
  gib = action["monthly_gib"]
  if gib is None:
    return None
  formula = c.saving_formula(action["gib_by_sku"], action["monthly_usd"])
  sources: List[Optional[Dict[str, Any]]] = []
  checks: List[Dict[str, Any]] = []
  if action["source"] == SOURCE_LEVER:
    fraction = action["stream_fraction"]
    formula.insert(
        0,
        f"{_gib(gib)}/mo = claimed stream bytes over {c.window} days ×"
        f" calibration {c.calibration} × {DAYS_PER_MONTH:g}/{c.window}"
        + (f" × {fraction:g} (share removed)." if fraction != 1.0 else "."),
    )
    sources, checks = c.stream_sources_and_checks(
        action["claims"], gib, fraction
    )
    if action["id"].startswith("stale_exclusion"):
      sources.append(
          _source(
              "log_router",
              "Log Router exclusions",
              "The exclusion rule this action is inferred from",
              [
                  "Open the _Default sink → Exclusions and compare each"
                  " filter's LOG_ID with the stream above."
              ],
              url=log_router_url(c.project),
              label="Open Log Router",
          )
      )
  else:
    pct = action["projected_savings_pct"]
    formula.insert(
        0,
        f"{_gib(gib)}/mo = {pct}% of the"
        f" {_gib(c.t30.get('monthly_run_rate_gib'))}/mo"
        f" {'invoiced' if c.invoiced else 'estimated'} run rate; {pct}% ="
        " bytes matching the filter ÷ all log content bytes in the Log"
        " Analytics sample window.",
    )
  if action.get("filter"):
    sources.append(
        _source(
            "logs_explorer",
            "What this filter would drop",
            "Preview the exact entries the exclusion matches",
            [
                "Runs the exclusion as a search over the sample window;"
                " everything listed would stop being ingested."
            ],
            query=action["filter"],
            language="logging_query",
            url=logs_explorer_url(c.project, action["filter"], f"P{c.window}D"),
            label="Open in Logs Explorer",
        )
    )
  sources.append(
      c.baseline_source(
          "Baseline run rate", "The monthly volume the saving is taken from"
      )
  )
  return _claim(
      f"action::{action['id']}",
      f"Saving: {action['title']}",
      f"{_money(action['monthly_usd'])}/mo · {_gib(gib)}/mo",
      "Volume measured from your own logs, priced against your"
      + c.priced_against,
      formula,
      sources + c.pricing_sources(),
      c.pricing_differences() + [_LATE_POINTS],
      checks,
  )


def build_provenance(summary: Dict[str, Any]) -> Dict[str, Any]:
  """Returns the `provenance` block for a finished summary."""
  c = _Ctx(summary)
  claims: Dict[str, Dict[str, Any]] = {}
  for claim in [
      _latest_complete_spend(c),
      _mtd_run_rate(c),
      _top_cost_driver(c),
      _trailing_30d_volume(c),
      _estimated_run_rate(c),
      _extraneous_spend(c),
      _service_mix(c),
      _severity_costs(c),
      *(_action(c, a) for a in c.actions),
  ]:
    if claim:
      claims[claim["id"]] = claim
  return {
      "billing_project": c.billing_project,
      "cross_project_billing": c.cross_project,
      "claims": claims,
  }
