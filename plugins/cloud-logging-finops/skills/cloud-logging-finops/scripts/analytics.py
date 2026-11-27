"""Log Analytics bucket detection, probe, breakdown queries and census samples."""

import collections
import concurrent.futures
import datetime
import json
import re
from typing import Any, Dict, List, Optional, Tuple

from constants import BYTES_PER_GIB
from constants import DEFAULT_BUCKET_ID
from constants import DEFAULT_LOCATION
from constants import DEFAULT_SAMPLE_DAYS
from constants import mask_sql
from constants import MAX_SAMPLES_PER_SEVERITY
from constants import PAYLOAD_BYTES_SQL
from constants import quote_table_ref
from constants import SIGNATURE_TEMPLATE_CHARS
from google.api_core import exceptions as api_exceptions
from google.cloud import bigquery
from google.cloud.logging_v2.services import config_service_v2

ConfigServiceV2Client = config_service_v2.ConfigServiceV2Client


def _parse_bucket_info(
    b: Any, loc: str, config_client: ConfigServiceV2Client
) -> Dict[str, Any]:
  """Extracts retention, analytics status and linked dataset from a bucket."""
  linked_dataset = None
  if b.analytics_enabled:
    try:
      for link in config_client.list_links(request={"parent": b.name}):
        if link.bigquery_dataset.dataset_id:
          linked_dataset = link.bigquery_dataset.dataset_id.rsplit("/", 1)[-1]
          break
    except api_exceptions.GoogleAPICallError as e:
      # The bucket's own name still resolves its view without the link.
      print(f"Notice: unable to list links for {b.name}: {e}")

  return {
      "name": b.name,
      "bucket_id": b.name.rsplit("/", 1)[-1],
      "location": loc,
      "analytics_enabled": bool(b.analytics_enabled),
      # Unset (0) means the default retention.
      "retention_days": int(b.retention_days or 30),
      "linked_dataset": linked_dataset,
  }


def detect_log_analytics_buckets(
    config_client: ConfigServiceV2Client,
    project_id: str,
    location: str = DEFAULT_LOCATION,
) -> List[Dict[str, Any]]:
  """Detects log buckets, their Log Analytics status and linked datasets."""
  detected_buckets = []
  locations_to_try = (
      [location] if location == "global" else [location, "global"]
  )

  for loc in locations_to_try:
    parent = f"projects/{project_id}/locations/{loc}"
    try:
      buckets = config_client.list_buckets(request={"parent": parent})
      for b in buckets:
        detected_buckets.append(_parse_bucket_info(b, loc, config_client))
    except api_exceptions.GoogleAPICallError as e:
      print(f"Notice: Unable to list buckets in location '{loc}': {e}")

  if not detected_buckets:
    for loc in locations_to_try:
      bucket_path = (
          f"projects/{project_id}/locations/{loc}/buckets/{DEFAULT_BUCKET_ID}"
      )
      try:
        b = config_client.get_bucket(request={"name": bucket_path})
      except api_exceptions.GoogleAPICallError:
        continue
      detected_buckets.append(_parse_bucket_info(b, loc, config_client))
      break

  detected_buckets.sort(
      key=lambda b: (
          b["bucket_id"] != DEFAULT_BUCKET_ID,
          not b["linked_dataset"],
          not b["analytics_enabled"],
      )
  )
  return detected_buckets


# The probe only sees the last `sample_days`, and the oldest entry inside that
# window lands a little after its start, so a full window reads slightly short.
MATURITY_TOLERANCE_DAYS = 0.5

_NO_DATA = {
    "status": "too_fresh",
    "days_available": 0.0,
    "earliest_log": None,
    "latest_log": None,
    "total_entries": 0,
}


def probe_log_analytics_data(
    bq_client: bigquery.Client,
    project_id: str,
    location: str = DEFAULT_LOCATION,
    bucket_id: str = DEFAULT_BUCKET_ID,
    sample_days: int = DEFAULT_SAMPLE_DAYS,
    now: Optional[datetime.datetime] = None,
    linked_dataset: Optional[str] = None,
) -> Dict[str, Any]:
  """Probes the Log Analytics view for data volume, age and maturity tier.

  Args:
    bq_client: BigQuery client.
    project_id: project owning the bucket.
    location: bucket location.
    bucket_id: Log Analytics bucket.
    sample_days: lookback window in days.
    now: current time; defaults to now (UTC).
    linked_dataset: linked BigQuery dataset, tried first.

  Returns:
    The probe result. Its `table_name` is the view that answered (unquoted),
    or None if none did; the breakdown and Prove It query that same view.
  """
  if now is None:
    now = datetime.datetime.now(datetime.timezone.utc)

  dataset = "default_logs" if bucket_id == "_Default" else f"{bucket_id}_logs"
  candidate_tables = [
      f"{project_id}.{linked_dataset}._AllLogs" if linked_dataset else None,
      f"{project_id}.{bucket_id}._AllLogs",
      f"{project_id}.{location}.{bucket_id}._AllLogs",
      f"{project_id}.{dataset}._AllLogs",
  ]
  job_config = bigquery.QueryJobConfig(
      query_parameters=[bigquery.ScalarQueryParameter("now", "TIMESTAMP", now)]
  )
  bq_loc = None if location == "global" else location

  last_error = None
  for table_name in dict.fromkeys(filter(None, candidate_tables)):
    # Timestamps and a row count only: maturity depends on nothing else, and
    # summing payload bytes here would scan every payload column.
    query = f"""
    SELECT
      MIN(timestamp) AS earliest_log,
      MAX(timestamp) AS latest_log,
      COUNT(1) AS total_entries,
      TIMESTAMP_DIFF(@now, MIN(timestamp), HOUR) AS hours_available
    FROM {quote_table_ref(table_name)}
    WHERE timestamp >= TIMESTAMP_SUB(@now, INTERVAL {sample_days} DAY)
    """
    try:
      rows = list(
          bq_client.query(
              query, location=bq_loc, job_config=job_config
          ).result()
      )
    except api_exceptions.GoogleAPICallError as e:
      # The view may live under any of the candidate names.
      last_error = e
      continue
    if not rows or not rows[0]["total_entries"]:
      return {**_NO_DATA, "table_name": table_name}

    row = rows[0]
    hours = float(row["hours_available"])
    days = round(hours / 24.0, 1)
    if hours < 24:
      status = "too_fresh"
    elif days < sample_days - MATURITY_TOLERANCE_DAYS:
      status = "partial_window"
    else:
      status = "mature"
    return {
        "status": status,
        "days_available": days,
        "earliest_log": row["earliest_log"].isoformat(),
        "latest_log": row["latest_log"].isoformat(),
        "total_entries": int(row["total_entries"]),
        "table_name": table_name,
    }

  print(f"Notice: Log Analytics probe query encountered: {last_error}")
  return {**_NO_DATA, "table_name": None}


def _strip_nulls(value: Any) -> Any:
  """Recursively drops null, empty-object and empty-array fields."""
  if isinstance(value, dict):
    cleaned = {k: _strip_nulls(v) for k, v in value.items()}
    return {k: v for k, v in cleaned.items() if v not in (None, {}, [])}
  if isinstance(value, list):
    cleaned = [_strip_nulls(v) for v in value]
    return [v for v in cleaned if v not in (None, {}, [])]
  return value


def _clean_payload(value: Optional[str]) -> Any:
  """Returns a payload column's real content, or None if it has none."""
  # `TO_JSON_STRING(NULL)` yields "null", and the `_AllLogs` proto_payload
  # struct serialises as a skeleton of null fields even when the entry has no
  # proto content. Both are treated as absent.
  if not value or not value.strip():
    return None
  try:
    parsed = json.loads(value)
  except ValueError:
    return value
  return _strip_nulls(parsed) or None


def _format_payload(value: Any) -> str:
  if isinstance(value, (dict, list)):
    return json.dumps(value, indent=2)
  return str(value)


def _truncate(text: str) -> str:
  return text if len(text) <= 2000 else text[:2000] + "... [truncated]"


def _parse_sample_log_from_bq_row(r: Any) -> Dict[str, Any]:
  """Parses the sample entry carried by one signature row."""
  ts = r["sample_timestamp"]
  labels = r["sample_resource_labels"]  # TO_JSON_STRING, so valid JSON.
  text_payload = r["sample_text_payload"]
  json_payload = _clean_payload(r["sample_json_payload"])
  proto_payload = _clean_payload(r["sample_proto_payload"])

  if text_payload:
    payload_str, payload_type = text_payload, "text"
  elif json_payload is not None:
    payload_str, payload_type = _format_payload(json_payload), "json"
  elif proto_payload is not None:
    payload_str, payload_type = _format_payload(proto_payload), "proto"
  else:
    payload_str, payload_type = r["signature_preview"], "text"

  return {
      "timestamp": ts.isoformat() if ts else None,
      "log_name": r["sample_log_name"].rsplit("/", 1)[-1],
      "resource_type": r["service"],
      "resource_labels": json.loads(labels) if labels else {},
      "payload": _truncate(payload_str),
      "payload_type": payload_type,
  }


_CONTROL_CHARS = re.compile(r"[\x00-\x1f\x7f-\x9f]")

# Artifacts of the SQL COALESCE falling through, not real messages.
_EMPTY_PREVIEWS = ("structured_payload", "null", "\\r\\n", "...")

_SYSLOG_PREFIX = re.compile(
    r"^[A-Z][a-z]{2}\s+\d+\s+\d+:\d+:\d+\s+[\w\-\.]+\s+([^:]+:\s*.+)$"
)

_TITLE_CHARS = 80


def _shape_title(preview: str) -> Tuple[str, str]:
  """Renders a JSON key skeleton as a de-duplicated field list."""
  keys = list(dict.fromkeys(k.strip() for k in preview.split(",") if k.strip()))
  if not keys:
    return "Structured record", preview
  shown = ", ".join(keys[:6])
  suffix = f" +{len(keys) - 6} more" if len(keys) > 6 else ""
  return f"Structured record ({len(keys)} fields): {shown}{suffix}", preview


def derive_display_text(sig: Dict[str, Any]) -> Tuple[str, str]:
  """Derives a display-only `(title, preview)` for a signature."""
  # Never build a filter from the result: it is cleaned and may not match the
  # rows the volume was measured over.
  raw = sig["preview"].strip()
  # A shape cluster's preview is a key skeleton, not prose.
  if sig["signature_source"] == "json_shape":
    return _shape_title(raw)

  clean = _CONTROL_CHARS.sub("", raw).strip()
  # A syslog timestamp and hostname are identical across every line in the
  # cluster, so they push the informative part out of the title.
  syslog_match = _SYSLOG_PREFIX.match(clean)
  if syslog_match:
    clean = syslog_match.group(1).strip()

  if not clean or clean in _EMPTY_PREVIEWS:
    log_id = sig["log_id"]
    label = log_id if log_id != "unknown" else sig["service"]
    return f"{sig['severity']} log in {label}", (clean or raw)

  title = clean[:_TITLE_CHARS].rstrip()
  if len(clean) > _TITLE_CHARS:
    title += "..."
  return title, clean


def build_samples_from_signatures(
    sigs: List[Dict[str, Any]],
) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
  """Selects representative log patterns per service and severity."""
  # Display-only census: cards carry no exclusion filter.
  by_service: Dict[str, Dict[str, List[Dict[str, Any]]]] = (
      collections.defaultdict(lambda: collections.defaultdict(list))
  )

  for s in sigs:
    title, preview = derive_display_text(s)
    by_service[s["service"]][s["severity"]].append({
        "title": title,
        "log_id": s["log_id"],
        "entry_count": s["count"],
        "total_bytes": s["total_bytes"],
        "total_gib": round(s["total_bytes"] / BYTES_PER_GIB, 2),
        # Not rendered as a filter; tells the reader what the pattern matched.
        "signature_source": s["signature_source"],
        "volume_measured": s["total_bytes"] > 0 or s["count"] > 0,
        "sample_log": s["sample_log"],
        "preview": preview,
    })

  out: Dict[str, Dict[str, List[Dict[str, Any]]]] = {}
  for srv, sevs in by_service.items():
    out[srv] = {}
    for sev, cards in sevs.items():
      cards.sort(
          key=lambda c: (c["total_bytes"], c["entry_count"]), reverse=True
      )
      out[srv][sev] = cards[:MAX_SAMPLES_PER_SEVERITY]
  return out


def format_logging_entry(
    entry: Any,
    service: str,
    severity: str,
) -> Dict[str, Any]:
  """Formats a `google.cloud.logging_v2` entry into a census sample item."""
  log_id = (entry.log_name or "unknown").rsplit("/", 1)[-1]
  res = entry.resource
  payload_val = entry.payload
  if isinstance(payload_val, dict):  # StructEntry
    payload_str, payload_type = json.dumps(payload_val, indent=2), "json"
  elif payload_val is not None:
    payload_str, payload_type = str(payload_val), "text"
  else:
    payload_str, payload_type = "", "empty"
  payload_str = _truncate(payload_str)

  return {
      "title": f"Recent {severity} log in {service} ({log_id})",
      "log_id": log_id,
      # API fallback samples carry no measured volume.
      "total_bytes": 0,
      "total_gib": 0.0,
      "entry_count": 0,
      "signature_source": "none",
      "volume_measured": False,
      "sample_log": {
          "timestamp": entry.timestamp.isoformat() if entry.timestamp else None,
          "log_name": log_id,
          "resource_type": res.type if res else service,
          "resource_labels": dict(res.labels or {}) if res else {},
          "payload": payload_str,
          "payload_type": payload_type,
      },
      "preview": payload_str[:120],
  }


_SAMPLE_FETCH_WORKERS = 8
_MAX_SAMPLE_PAIRS = 24


def _list_recent_entries(
    logging_client: Any,
    resource_names: List[str],
    filter_str: str,
    max_results: int,
) -> List[Any]:
  """Returns the newest `max_results` entries matching a filter."""
  return list(
      logging_client.list_entries(
          resource_names=resource_names,
          filter_=filter_str,
          order_by="timestamp desc",
          page_size=max_results,
          max_results=max_results,
      )
  )


def fetch_logging_api_samples(
    logging_client: Any,
    project_id: str,
    top_services: List[str],
    parsed_severity: Dict[str, Dict[str, Any]],
    samples_by_service: Dict[str, Dict[str, List[Dict[str, Any]]]],
    now: Optional[datetime.datetime] = None,
    lookback_days: int = DEFAULT_SAMPLE_DAYS,
    read_scope: Optional[Dict[str, Any]] = None,
) -> Dict[str, Dict[str, str]]:
  """Fetches recent log entries via the Logging API for streams with no census.

  Measured census cards are never replaced. Pairs are read concurrently and
  capped at `_MAX_SAMPLE_PAIRS`.

  Args:
    logging_client: A `google.cloud.logging_v2.Client`.
    project_id: Project whose entries are read.
    top_services: Resource types to sample, in rank order.
    parsed_severity: Severities observed per service; picks which to sample.
    samples_by_service: Filled in place with formatted samples.
    now: Reference instant for the read window. Defaults to the current time.
    lookback_days: Length of the read window; matches the severity breakdown.
    read_scope: From `inventory.resolve_log_read_scope`. Defaults to the
      project's own buckets.

  Returns:
    `{service: {severity: message}}` explaining each pair that yielded no
    samples (API error or empty window).
  """
  sample_errors: Dict[str, Dict[str, str]] = collections.defaultdict(dict)
  if not top_services:
    return {}

  pairs = []
  for srv in top_services:
    if srv not in samples_by_service:
      samples_by_service[srv] = {}

    sevs = list(parsed_severity.get(srv, {}).keys())
    if not sevs:
      sevs = ["INFO", "ERROR", "WARNING", "DEBUG", "DEFAULT"]

    for sev in sevs:
      if samples_by_service[srv].get(sev):
        continue
      pairs.append((srv, sev))

  if not pairs:
    return {}
  # Ordered by service rank already, so the truncation drops the least
  # significant streams rather than an arbitrary slice.
  pairs = pairs[:_MAX_SAMPLE_PAIRS]

  log_scope = (read_scope or {}).get("log_scope")
  resource_names = list(
      (read_scope or {}).get("resource_names") or [f"projects/{project_id}"]
  )
  scoped = (read_scope or {}).get("source") == "default_scope"

  # `list_entries` silently narrows any filter without a `timestamp` clause to
  # the last 24 hours; state the breakdown's window instead.
  now = now or datetime.datetime.now(datetime.timezone.utc)
  start = now - datetime.timedelta(days=lookback_days)
  window_filter = f'timestamp >= "{start.strftime("%Y-%m-%dT%H:%M:%SZ")}"'
  empty_message = f"No log entries in the last {lookback_days} days."
  where = f"projects/{project_id}"
  required_roles = "roles/logging.viewer"
  if scoped:
    # A log scope can span other projects' views. Only this project's entries
    # describe the volume being audited, so samples are limited to them.
    window_filter = (
        f'logName:"projects/{project_id}/logs/" AND {window_filter}'
    )
    empty_message = (
        f"No log entries from {project_id} in the last {lookback_days} days"
        f" in log scope {log_scope}."
    )
    where = f"log scope {log_scope}"
    required_roles += " (and roles/logging.viewAccessor on its log views)"

  # One cheap read first. If the project cannot be read at all, every stream
  # would fail the same way, so there is no point issuing the rest.
  try:
    probe = _list_recent_entries(
        logging_client, resource_names, window_filter, max_results=1
    )
  except Exception as e:  # pylint: disable=broad-except
    print(
        "[FINOPS ADVISORY] Representative logs unavailable: could not read"
        f" log entries in {where} ({e}). Reading entries requires"
        f" {required_roles}. Service Details will show this error instead"
        " of samples."
    )
    probe, empty_message = [], str(e)
  if not probe:
    for srv, sev in pairs:
      sample_errors[srv][sev] = empty_message
    return dict(sample_errors)

  def fetch_pair(srv: str, sev: str) -> None:
    # DEFAULT is a real severity value, not a wildcard.
    filter_str = (
        f'resource.type = "{srv}" AND severity = "{sev}" AND {window_filter}'
    )
    try:
      entries = _list_recent_entries(
          logging_client, resource_names, filter_str, MAX_SAMPLES_PER_SEVERITY
      )
    except Exception as e:  # pylint: disable=broad-except
      # One unreadable stream must not cost the others their samples.
      print(
          "Notice: Could not fetch sample logs via Logging API for"
          f" {srv}/{sev}: {e}"
      )
      sample_errors[srv][sev] = str(e)
      return
    if entries:
      samples_by_service[srv][sev] = [
          format_logging_entry(entry, srv, sev) for entry in entries
      ]
    else:
      sample_errors[srv][sev] = empty_message

  with concurrent.futures.ThreadPoolExecutor(
      max_workers=min(_SAMPLE_FETCH_WORKERS, len(pairs))
  ) as executor:
    list(executor.map(lambda pair: fetch_pair(*pair), pairs))
  return dict(sample_errors)


def query_log_analytics_breakdown(
    bq_client: bigquery.Client,
    table_name: str,
    sample_days: int = DEFAULT_SAMPLE_DAYS,
    location: str = DEFAULT_LOCATION,
) -> Dict[str, Any]:
  """Runs the Log Analytics severity, log name and signature queries."""
  table = quote_table_ref(table_name)
  window = (
      f"timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {sample_days}"
      " DAY)"
  )
  log_id_sql = (
      "COALESCE(log_id, REGEXP_EXTRACT(log_name, r'logs/([^/]+)$'), 'unknown')"
  )
  severity_sql = f"""
          SELECT
            COALESCE(resource.type, 'unknown') AS service,
            COALESCE(severity, 'DEFAULT') AS severity,
            FORMAT_DATE('%Y-%m-%d', DATE(timestamp)) AS log_date,
            COUNT(1) AS entry_count,
            SUM({PAYLOAD_BYTES_SQL}) AS total_bytes
          FROM {table}
          WHERE {window}
          GROUP BY service, severity, log_date
          ORDER BY service, log_date
      """
  log_names_sql = f"""
          SELECT
            COALESCE(resource.type, 'unknown') AS service,
            {log_id_sql} AS log_id,
            COALESCE(severity, 'DEFAULT') AS severity,
            COUNT(1) AS entry_count
          FROM {table}
          WHERE {window}
          GROUP BY service, log_id, severity
          ORDER BY entry_count DESC
          LIMIT 100
      """
  signatures_sql = f"""
          WITH extracted AS (
            SELECT
              COALESCE(resource.type, 'unknown') AS service,
              {log_id_sql} AS log_id,
              COALESCE(severity, 'DEFAULT') AS severity,
              -- JSON_VALUE is case-sensitive, and systemd writes MESSAGE.
              COALESCE(
                text_payload,
                JSON_VALUE(json_payload.message),
                JSON_VALUE(json_payload.MESSAGE),
                JSON_VALUE(json_payload.msg),
                JSON_VALUE(json_payload.log),
                proto_payload.audit_log.method_name
              ) AS raw_message,
              -- Mirrors the COALESCE above so filters target the right field.
              CASE
                WHEN text_payload IS NOT NULL THEN 'text_payload'
                WHEN JSON_VALUE(json_payload.message) IS NOT NULL THEN 'json_message'
                WHEN JSON_VALUE(json_payload.MESSAGE) IS NOT NULL THEN 'json_MESSAGE'
                WHEN JSON_VALUE(json_payload.msg) IS NOT NULL THEN 'json_msg'
                WHEN JSON_VALUE(json_payload.log) IS NOT NULL THEN 'json_log'
                WHEN proto_payload.audit_log.method_name IS NOT NULL THEN 'audit_method'
                WHEN json_payload IS NOT NULL THEN 'json_shape'
                WHEN proto_payload.type IS NOT NULL THEN 'proto_type'
                ELSE 'none'
              END AS signature_source,
              -- Key skeleton for message-less JSON. DISTINCT + ORDER BY
              -- canonicalise it so key order/repetition don't split groups.
              ARRAY_TO_STRING(
                ARRAY(
                  SELECT DISTINCT k
                  FROM UNNEST(
                    REGEXP_EXTRACT_ALL(
                      TO_JSON_STRING(json_payload), r'"([^"]+)":'
                    )
                  ) AS k
                  ORDER BY k
                ),
                ','
              ) AS json_shape,
              proto_payload.type AS proto_type,
              timestamp, text_payload, json_payload, proto_payload,
              log_name, resource
            FROM {table}
            WHERE {window}
          ),
          templated AS (
            SELECT
              *,
              SUBSTR(
                COALESCE(
                  -- Audit method names are already canonical; masking them
                  -- would fold v1/v2/v3 of an API onto one template.
                  IF(signature_source = 'audit_method',
                     raw_message,
                     {mask_sql('raw_message')}),
                  NULLIF(json_shape, ''),
                  proto_type,
                  'structured_payload'
                ),
                1, {SIGNATURE_TEMPLATE_CHARS}
              ) AS signature_preview
            FROM extracted
          ),
          grouped_signatures AS (
            SELECT
              service,
              log_id,
              severity,
              signature_preview,
              signature_source,
              COUNT(1) AS entry_count,
              SUM({PAYLOAD_BYTES_SQL}) AS total_bytes,
              -- One ANY_VALUE(STRUCT) so all sample fields come from one row.
              ANY_VALUE(STRUCT(
                timestamp AS sample_timestamp,
                text_payload AS sample_text_payload,
                TO_JSON_STRING(json_payload) AS sample_json_payload,
                TO_JSON_STRING(proto_payload) AS sample_proto_payload,
                TO_JSON_STRING(resource.labels) AS sample_resource_labels,
                log_name AS sample_log_name
              )) AS sample_entry
            FROM templated
            GROUP BY service, log_id, severity, signature_preview, signature_source
          ),
          ranked_signatures AS (
            SELECT *,
              SUM(total_bytes) OVER (PARTITION BY service, severity, log_id) AS stream_total_bytes,
              SUM(entry_count) OVER (PARTITION BY service, severity, log_id) AS stream_entry_count,
              ROW_NUMBER() OVER (PARTITION BY service, severity ORDER BY total_bytes DESC) AS rank_in_sev,
              ROW_NUMBER() OVER (ORDER BY total_bytes DESC) AS global_rank
            FROM grouped_signatures
          )
          SELECT
            * EXCEPT (sample_entry, rank_in_sev, global_rank),
            sample_entry.*
          FROM ranked_signatures
          -- Wider than rendered: the optimizer dedupes clusters per rule.
          WHERE rank_in_sev <= 15 OR global_rank <= 30
          ORDER BY total_bytes DESC
      """

  bq_loc = None if location == "global" else location
  with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    severity_rows, log_name_rows, signature_rows = pool.map(
        lambda sql: list(bq_client.query(sql, location=bq_loc).result()),
        (severity_sql, log_names_sql, signatures_sql),
    )

  # One unit for the whole result set, so bytes and entries never mix.
  by_bytes = any(r["total_bytes"] > 0 for r in severity_rows)
  volume_column = "total_bytes" if by_bytes else "entry_count"

  parsed_sev: Dict[str, Dict[str, List[List[Any]]]] = collections.defaultdict(
      lambda: collections.defaultdict(list)
  )
  for r in severity_rows:
    parsed_sev[r["service"]][r["severity"]].append(
        [r["log_date"], int(r[volume_column])]
    )

  top_logs: Dict[str, List[Dict[str, Any]]] = collections.defaultdict(list)
  for r in log_name_rows:
    top_logs[r["service"]].append({
        "log_id": r["log_id"],
        "severity": r["severity"],
        "count": int(r["entry_count"]),
    })

  sigs = [
      {
          "service": r["service"],
          "log_id": r["log_id"],
          "severity": r["severity"],
          "preview": r["signature_preview"],
          "count": int(r["entry_count"]),
          "total_bytes": int(r["total_bytes"]),
          "stream_total_bytes": int(r["stream_total_bytes"]),
          "stream_entry_count": int(r["stream_entry_count"]),
          "signature_source": r["signature_source"],
          "sample_log": _parse_sample_log_from_bq_row(r),
      }
      for r in signature_rows
  ]

  return {
      "severity_history": {srv: dict(sevs) for srv, sevs in parsed_sev.items()},
      # The coverage denominator; never an entry count posing as bytes.
      "total_payload_bytes": (
          sum(int(r["total_bytes"]) for r in severity_rows) if by_bytes else 0
      ),
      "top_log_names": dict(top_logs),
      "top_signatures": sigs,
      "samples_by_service": build_samples_from_signatures(sigs),
  }
