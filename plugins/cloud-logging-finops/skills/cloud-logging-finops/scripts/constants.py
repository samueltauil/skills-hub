"""Domain constants and shared utility helpers for Cloud Logging FinOps."""

import json
import os
from typing import Any

# ==============================================================================
# Domain Constants
# ==============================================================================

# Cloud Logging is priced in gibibytes, not gigabytes (a 7.4% difference).
BYTES_PER_GIB = 1024.0**3
LIST_PRICE_PER_GIB = 0.50
FREE_TIER_GIB_PER_MONTH = 50.0

DEFAULT_SAMPLE_DAYS = 14
DEFAULT_ANALYSIS_MONTHS = 6
DEFAULT_TELEMETRY_LOOKBACK_DAYS = 30
DEFAULT_BUCKET_ID = "_Default"
DEFAULT_LOCATION = "global"

# Cloud Monitoring keeps `logging.googleapis.com/*` for 42 days and silently
# returns less when asked for more, so windows must be clamped.
MONITORING_RETENTION_DAYS = 42

DAYS_PER_MONTH = 30.0

LOGGING_SERVICE_NAME = "Cloud Logging"
LOGGING_SERVICE_ID = "5490-F7B7-8DF6"
INGESTION_SKU_NAME = "Cloud Logging - Log Volume"
ESTIMATED_SKU_NAME = f"{INGESTION_SKU_NAME} (Estimated)"

# Ingestion is billed per `gibibyte`, retention per `gibibyte month`, under the
# same service id; only the former is ingestion volume.
INGESTION_PRICING_UNIT = "gibibyte"

# Cloud Billing closes days and months on US/Pacific time, not UTC.
INVOICE_TIMEZONE = "America/Los_Angeles"

# One project's Cloud Logging rows in a billing export. The collector binds the
# placeholders as query parameters; Prove It inlines literals so the SQL it
# shows can be pasted as is.
LOGGING_SCOPE_SQL = (
    "(service.description = {service_name} OR service.id = {service_id})\n"
    "  AND project.id = {project_id}"
)


def bare_table_ref(table_ref: str) -> str:
  """Returns `project.dataset.table` without surrounding backticks."""
  return table_ref.strip().strip("`")


def quote_table_ref(table_ref: str) -> str:
  """Returns `table_ref` wrapped in exactly one pair of backticks."""
  # Hyphenated project ids can contain keywords (e.g. `a-with-b`), so every
  # table interpolated into SQL must be quoted.
  return f"`{bare_table_ref(table_ref)}`"


# ==============================================================================
# Byte Measurement
# ==============================================================================

# Authoritative volume metrics. Never use Log Analytics payload byte sums as a
# proxy for billed volume: they overstate it about 2x.
BILLED_BYTES_METRIC = "logging.googleapis.com/billing/bytes_ingested"
BYTE_COUNT_METRIC = "logging.googleapis.com/byte_count"

# Payload bytes for *content* analysis only (signature weighting, severity
# mix). `proto_payload` is a non-NULL STRUCT on every `_AllLogs` row, so the
# IF-guard skips its ~1 KB null skeleton when the row has no proto content.
# Not billed bytes: use BILLED_BYTES_METRIC for anything cost-facing.
PAYLOAD_BYTES_SQL = """
                COALESCE(BYTE_LENGTH(text_payload), 0) +
                COALESCE(BYTE_LENGTH(TO_JSON_STRING(json_payload)), 0) +
                IF(proto_payload.type IS NULL, 0,
                   COALESCE(BYTE_LENGTH(TO_JSON_STRING(proto_payload)), 0))
"""

# ==============================================================================
# Signature Templating
# ==============================================================================

# Masks variable tokens so lines group into templates. Order matters: each
# pattern runs on the previous one's output, so specific forms (dates, IPs)
# must match before the bare-integer rule.
SIGNATURE_MASK_PATTERNS = (
    (
        r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:?\d{2})?",
        "<TS>",
    ),
    (r"[A-Z][a-z]{2} +\d{1,2} \d{2}:\d{2}:\d{2}", "<TS>"),  # syslog
    (
        (
            r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}"
            r"-[0-9a-fA-F]{12}"
        ),
        "<UUID>",
    ),
    (r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", "<IP>"),
    (r"0x[0-9a-fA-F]+|\b[0-9a-fA-F]{8,}\b", "<HEX>"),
    (r"/[\w.\-]+/[\w./\-]*", "<PATH>"),
    # Blunt: also merges 'HTTP 500' with 'HTTP 200'.
    (r"\d+", "<N>"),
)

# A template containing a placeholder describes a family of lines, so it must
# never be interpolated into an exclusion filter as a literal.
MASK_PLACEHOLDERS = tuple(sorted({repl for _, repl in SIGNATURE_MASK_PATTERNS}))

# Templates are grouped and compared at this length.
SIGNATURE_TEMPLATE_CHARS = 200


def mask_sql(expr: str) -> str:
  """Wraps `expr` in the REGEXP_REPLACE chain that turns text into a template."""
  sql = expr
  for pattern, replacement in SIGNATURE_MASK_PATTERNS:
    sql = f"REGEXP_REPLACE({sql}, r'{pattern}', '{replacement}')"
  return sql


# ==============================================================================
# Extraneous Spend Model
# ==============================================================================

# GCP console default for VPC flow log sampling; lower targets would overstate
# recoverable spend.
FLOW_LOG_TARGET_SAMPLING = 0.5

# Free retention included with ingestion. Storage beyond this is billed extra.
INCLUDED_RETENTION_DAYS = 30

# If the computed floor exceeds this share of billable spend, still render it
# but flag it for manual review rather than presenting it as a safe number.
WASTE_SANITY_CEILING_PCT = 60.0

# Log IDs that are always free (stored in the _Required bucket). These must be
# excluded from both the numerator and denominator of any waste calculation.
FREE_REQUIRED_LOG_IDS = (
    "cloudaudit.googleapis.com/activity",
    "externalaudit.googleapis.com/activity",
    "cloudaudit.googleapis.com/system_event",
    "externalaudit.googleapis.com/system_event",
    "cloudaudit.googleapis.com/access_transparency",
    "externalaudit.googleapis.com/access_transparency",
)

# Buckets whose retention cannot be edited and is not billed (`_Required` is
# pinned at 400 days), so they are never reported as over-retained.
IMMUTABLE_RETENTION_BUCKETS = ("_Required",)

# Data Access audit logs are billed but often compliance-mandated, so they are
# surfaced to the owner and never counted as recoverable spend.
DATA_ACCESS_LOG_IDS = (
    "cloudaudit.googleapis.com/data_access",
    "externalaudit.googleapis.com/data_access",
)

# Streams still offered as actions, but read by security teams, so the reader
# is told what they are for. The value completes "Dropping this removes ...".
SECURITY_TELEMETRY_LOG_IDS = {
    "compute.googleapis.com/firewall": (
        "the record of which connections your firewall rules allowed and denied"
    ),
    "compute.googleapis.com/vpc_flows": (
        "the network flow record used for traffic forensics and incident"
        " reconstruction"
    ),
    "networkmanagement.googleapis.com/vpc_flows": (
        "the network flow record used for traffic forensics and incident"
        " reconstruction"
    ),
    "compute.googleapis.com/nat": (
        "the NAT translation record used to attribute outbound traffic to an"
        " instance"
    ),
    "dns.googleapis.com/dns_queries": (
        "the DNS query record used to detect exfiltration and command-and-"
        "control traffic"
    ),
    "cloudaudit.googleapis.com/policy": (
        "the record of requests your org policies denied"
    ),
}

# Payload markers of Linux audit subsystem records (often retained under
# PCI-DSS and FedRAMP), whose agent-chosen log ids cannot identify them.
HOST_AUDIT_PAYLOAD_MARKERS = (
    "type=PROCTITLE",
    "type=SYSCALL",
    "type=AVC",
    "audispd",
    "auditd.service",
)

HOST_AUDIT_CAVEAT = (
    "the Linux audit subsystem record of process and syscall activity on your"
    " instances"
)

# Display budget for patterns per (service, severity) in Service Details.
MAX_SAMPLES_PER_SEVERITY = 5

# Kept small: exclusions are irreversible and a long list invites bulk
# application without review.
MAX_EXCLUSION_CANDIDATES = 5


# ==============================================================================
# Pricing
# ==============================================================================

# A derived rate outside this band means volume and cost came from different
# bases, so it is rejected rather than published.
PLAUSIBLE_RATE_RANGE_PER_GIB = (0.05, 2.50)


def billable_gib(
    total_gib: float, free_tier_gib: float = FREE_TIER_GIB_PER_MONTH
) -> float:
  """Returns the portion of a month's ingestion that is actually charged."""
  return max(0.0, (total_gib or 0.0) - free_tier_gib)


def price_reduction(
    removed_gib: float,
    baseline_monthly_gib: float,
    rate_per_gib: float = LIST_PRICE_PER_GIB,
    free_tier_gib: float = FREE_TIER_GIB_PER_MONTH,
) -> float:
  """Returns the monthly saving from removing `removed_gib` of ingestion."""
  # The difference of two bills, so volume that falls back inside the free tier
  # saves nothing (100 GiB dropping 80 GiB saves $25, not $40).
  baseline = max(0.0, baseline_monthly_gib or 0.0)
  removed = max(0.0, min(removed_gib or 0.0, baseline))
  before = billable_gib(baseline, free_tier_gib)
  after = billable_gib(baseline - removed, free_tier_gib)
  return round((before - after) * rate_per_gib, 2)


def write_json(file_path: str, content: Any) -> None:
  """Helper to write content to a JSON file ensuring parent directories exist."""
  dir_name = os.path.dirname(file_path)
  if dir_name:
    os.makedirs(dir_name, exist_ok=True)
  with open(file_path, "w") as f:
    json.dump(content, f, indent=2)
