"""Extraneous log spend model for Cloud Logging FinOps.

Computes a conservative floor for recoverable spend from billing/bytes_ingested
and byte_count only; Log Analytics payload bytes overstate billed volume ~2x.
Each lever is emitted as an `actions.Action`; the headline is the sum of the
counted ones, priced on exactly the claims their remedy can act on.
"""

import re
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

from actions import Action
from actions import ALL_SEVERITIES
from actions import Claim
from actions import filter_from_claims
from actions import SOURCE_LEVER
from constants import billable_gib
from constants import BYTES_PER_GIB
from constants import FLOW_LOG_TARGET_SAMPLING
from constants import IMMUTABLE_RETENTION_BUCKETS
from constants import INCLUDED_RETENTION_DAYS
from constants import WASTE_SANITY_CEILING_PCT
from exclusion_rules import decode_log_id
from exclusion_rules import is_data_access
from exclusion_rules import is_free_required
import messages
from pricing import PriceBook

# Matches LOG_ID("...") / logName tokens inside a Log Router filter.
_LOG_ID_RE = re.compile(r'LOG_ID\(\s*"([^"]+)"\s*\)', re.IGNORECASE)
_LOG_NAME_RE = re.compile(r'logs/([^"\s$]+)', re.IGNORECASE)

# Max share a "dead" exclusion target may still carry (tolerates stragglers).
_DEAD_RULE_MAX_SHARE = 0.02

# Removing one of two destinations recovers half the billed bytes (a floor).
_DUPLICATE_COPY_FRACTION = 0.5

# Unfiltered sinks pair up combinatorially; evidence shows a sample plus count.
_MAX_EVIDENCE_PAIRS = 8

_LOG_ID_TERM = r'LOG_ID\(\s*"[^"]+"\s*\)'
# A sink filter of `NOT LOG_ID(...)` terms joined by AND, the shape of the stock
# `_Default` sink filter: "every stream but these".
_EXCLUSION_ONLY_FILTER_RE = re.compile(
    rf"^\s*NOT\s+{_LOG_ID_TERM}(\s+AND\s+NOT\s+{_LOG_ID_TERM})*\s*$",
    re.IGNORECASE,
)
# A sink exclusion of `LOG_ID(...)` terms joined by OR: drops whole streams.
_WHOLE_STREAM_EXCLUSION_RE = re.compile(
    rf"^\s*{_LOG_ID_TERM}(\s+OR\s+{_LOG_ID_TERM})*\s*$", re.IGNORECASE
)


class _ClaimLedger:
  """Prevents two levers from counting the same bytes twice.

  Each stream can be claimed at most once in total. `retain` records that only
  part of a stream stays billed (e.g. after dedup), scaling later claims.
  """

  def __init__(self) -> None:
    self._claimed: Dict[str, float] = {}
    self._retained: Dict[str, float] = {}

  def retain(self, key: str, factor: float) -> None:
    """Records that only `factor` of `key`'s bytes stay billed hereafter."""
    self._retained[key] = self.retained(key) * max(0.0, min(1.0, factor))

  def retained(self, key: str) -> float:
    return self._retained.get(key, 1.0)

  def claim(self, key: str, fraction: float) -> float:
    """Claims up to `fraction` of `key`'s billed rest; returns the share won."""
    # The returned share is relative to all of `key`'s bytes.
    fraction = max(0.0, min(1.0, fraction)) * self.retained(key)
    already = self._claimed.get(key, 0.0)
    granted = max(0.0, min(fraction, 1.0 - already))
    if granted > 0:
      self._claimed[key] = already + granted
    return granted


def _log_ids_in_filter(filter_expr: str) -> List[str]:
  """Extracts referenced log IDs, decoded, from a Log Router filter."""
  found = _LOG_ID_RE.findall(filter_expr or "")
  found += _LOG_NAME_RE.findall(filter_expr or "")
  return [decode_log_id(f).rstrip("$") for f in found]


def _stream_suffix(log_id: str) -> str:
  """Returns the service-independent suffix of a log ID."""
  # `compute.googleapis.com/vpc_flows` and
  # `networkmanagement.googleapis.com/vpc_flows` share the suffix `vpc_flows`,
  # which identifies a migrated stream as the successor of an excluded one.
  return log_id.rsplit("/", 1)[-1].lower()


def _sink_streams(
    sink: Dict[str, Any], log_ids: Set[str]
) -> Optional[Set[str]]:
  """Returns the log IDs a bucket sink provably stores, or None if unknown."""
  # Only empty filters and conjunctions of `NOT LOG_ID(...)` are evaluated, and
  # only whole-stream `LOG_ID(...)` exclusions are subtracted.
  expr = (sink.get("filter") or "").strip()
  if not expr:
    routed = set(log_ids)
  elif _EXCLUSION_ONLY_FILTER_RE.match(expr):
    routed = log_ids - set(_log_ids_in_filter(expr))
  else:
    return None
  for exclusion in sink.get("exclusions") or ():
    if exclusion.get("disabled"):
      continue
    excluded = (exclusion.get("filter") or "").strip()
    if not _WHOLE_STREAM_EXCLUSION_RE.match(excluded):
      return None
    routed -= set(_log_ids_in_filter(excluded))
  return routed


def _duplicate_pairs(
    sinks: Sequence[Dict[str, Any]], log_ids: Set[str]
) -> List[Tuple[str, str, Set[str]]]:
  """Returns `(a, b, overlap)` for bucket-sink pairs billing streams twice."""
  # Ingestion is billed per destination bucket. Only pairs whose overlap is
  # provable and non-empty are returned.
  routed = []
  for sink in sinks:
    if (
        "logging.googleapis.com" not in str(sink.get("destination", ""))
        or sink.get("name") == "_Required"
        or sink.get("disabled")
    ):
      continue
    streams = _sink_streams(sink, log_ids)
    if streams:
      routed.append((str(sink.get("name")), streams))
  pairs = []
  for i, (first, first_streams) in enumerate(routed):
    for second, second_streams in routed[i + 1 :]:
      overlap = first_streams & second_streams
      if overlap:
        pairs.append((first, second, overlap))
  return pairs


def _format_pairs(pairs: Sequence[Tuple[str, str, Set[str]]]) -> str:
  """Renders sink pairs for evidence prose, bounded to a readable sample."""
  shown = ", ".join(f"{a} + {b}" for a, b, _ in pairs[:_MAX_EVIDENCE_PAIRS])
  remainder = len(pairs) - _MAX_EVIDENCE_PAIRS
  if remainder > 0:
    return f"{shown}, and {remainder} more pair(s)"
  return shown


def compute_extraneous_spend(
    billed_by_service: Dict[str, float],
    byte_count_by_stream: Dict[Tuple[str, str], float],
    window_days: float,
    monthly_gib: float,
    price_book: PriceBook,
    project_id: str,
    sinks: Optional[Sequence[Dict[str, Any]]] = None,
    exclusions: Optional[Sequence[Dict[str, Any]]] = None,
    buckets: Optional[Sequence[Dict[str, Any]]] = None,
    flow_log_configs: Optional[Sequence[Dict[str, Any]]] = None,
    billed_window_gib: Optional[float] = None,
) -> Tuple[Dict[str, Any], List[Action]]:
  """Computes the conservative extraneous-spend floor and its lever actions.

  Args:
    billed_by_service: bytes from billing/bytes_ingested keyed by resource type,
      over the sample window.
    byte_count_by_stream: bytes from byte_count keyed by (log_id, severity).
    window_days: length of the measurement window in days.
    monthly_gib: gross monthly ingestion run-rate used as the baseline.
    price_book: per-SKU prices and baselines every saving is priced from.
    project_id: project the exclusion filters target.
    sinks: Log Router sinks.
    exclusions: project-level exclusions.
    buckets: log buckets with retention metadata.
    flow_log_configs: VPC flow log configs from the Compute / Network Management
      APIs.
    billed_window_gib: invoiced ingestion over the same window; preferred
      calibration anchor so numerator and (invoiced) denominator share a basis.

  Returns:
    `(extraneous_spend, lever_actions)`: the report contract, and the actions
    to pass to `actions.merge_actions`.
  """
  billable_monthly_gib = billable_gib(monthly_gib)
  if not byte_count_by_stream or billable_monthly_gib <= 0:
    return {
        "status": "insufficient_data",
        "reason": (
            "Authoritative volume metrics unavailable; refusing to estimate."
        ),
    }, []

  # Decoded once here so every comparison below is on plain IDs. Always-free
  # _Required streams are left out of every calculation.
  billable_streams: Dict[Tuple[str, str], float] = {}
  for (log_id, severity), num_bytes in byte_count_by_stream.items():
    key = (decode_log_id(log_id), severity)
    if not is_free_required(key[0]):
      billable_streams[key] = billable_streams.get(key, 0.0) + num_bytes

  # byte_count (received, carries log/severity labels) exceeds billed bytes by
  # ~1.5x, so rescale it onto the billed basis. Prefer the invoice as anchor.
  raw_stream_total = sum(billable_streams.values()) or 1.0
  if billed_window_gib is not None and billed_window_gib > 0:
    billed_total = billed_window_gib * BYTES_PER_GIB
  else:
    billed_total = sum(billed_by_service.values()) if billed_by_service else 0.0
  # Only ever scale down: if billed exceeds byte_count the labels are
  # incomplete, and inflating measured bytes would invent savings.
  calibration = min(
      billed_total / raw_stream_total if billed_total > 0 else 1.0, 1.0
  )
  billable_streams = {k: v * calibration for k, v in billable_streams.items()}
  total_stream_bytes = sum(billable_streams.values()) or 1.0

  bytes_by_log: Dict[str, float] = {}
  for (log_id, _), num_bytes in billable_streams.items():
    bytes_by_log[log_id] = bytes_by_log.get(log_id, 0.0) + num_bytes

  days = window_days if window_days > 0 else 1.0

  def monthly(num_bytes: float) -> float:
    return num_bytes / days * 30.0 / BYTES_PER_GIB

  def measured(log_id: str, severity: str) -> float:
    if severity == ALL_SEVERITIES:
      return bytes_by_log[log_id]
    return billable_streams[(log_id, severity)]

  ledger = _ClaimLedger()
  levers: List[Action] = []

  def add(
      lever_id: str,
      title: str,
      evidence: str,
      claims: Sequence[Tuple[str, str, float]] = (),
      manual_step: str = "",
      withheld: str = "",
      counted: bool = True,
      **kwargs: Any,
  ) -> None:
    """Prices one lever on the claims its remedy can act on."""
    # `claims` are `(log_id, severity|"*", window_bytes)`. A lever without a
    # manual step is remedied by an exclusion filter, so its claims pass the
    # same safety gate as every exclusion before anything is priced.
    claimed = [Claim(l, s, monthly(b)) for l, s, b in claims if b > 0]
    action = Action(
        id=lever_id,
        title=title,
        source=SOURCE_LEVER,
        evidence=evidence,
        manual_step=manual_step,
        withheld=withheld,
        **kwargs,
    )
    if manual_step or withheld:
      action.claims = claimed
    else:
      action.filter, action.claims, action.refused_claims = filter_from_claims(
          claimed, project_id
      )
      if not action.claims:
        action.withheld = messages.WITHHELD_NO_REMEDY
    gib = sum(c.monthly_gib for c in action.claims)
    action.counted = counted and gib > 0 and not action.withheld
    if gib > 0:
      gib_by_sku = price_book.split_by_logs(
          gib, ((c.log_id, c.monthly_gib) for c in action.claims)
      )
      action.monthly_gib = round(gib, 2)
      action.monthly_usd = price_book.saving(gib_by_sku)
      # Share of spend, not of volume: SKUs are priced differently.
      action.pct_of_billable = price_book.pct_of_spend(action.monthly_usd)
      action.gib_by_sku = {k: round(v, 2) for k, v in gib_by_sku.items() if v}
      # Prove It re-measures whole streams and scales by this share.
      stream_gib = sum(
          monthly(measured(c.log_id, c.severity)) for c in action.claims
      )
      action.stream_fraction = round(gib / stream_gib, 4)
    levers.append(action)

  # --- Duplicate bucket routing (billing mechanics) --------------------------
  dup_pairs = _duplicate_pairs(sinks or (), set(bytes_by_log))
  if dup_pairs:
    # Calibrated stream bytes include every copy; claim half (floor) of the
    # streams some pair provably routes twice.
    dup_claims = []
    for log_id in sorted(set().union(*(o for _, _, o in dup_pairs))):
      granted = ledger.claim(log_id, _DUPLICATE_COPY_FRACTION)
      ledger.retain(log_id, 1.0 - _DUPLICATE_COPY_FRACTION)
      dup_claims.append(
          (log_id, ALL_SEVERITIES, bytes_by_log[log_id] * granted)
      )
    add(
        "duplicate_bucket_routing",
        "Duplicate log bucket routing",
        "Sink pairs route the same streams to separate log buckets, and GCP"
        " bills ingestion once per destination bucket: "
        + _format_pairs(dup_pairs),
        dup_claims,
        manual_step=(
            "Add an exclusion to the redundant sink so each entry is billed to"
            " one destination bucket (google_logging_project_sink.exclusions)."
        ),
    )

  # --- Retention beyond the included 30 days (not measurable here) -----------
  over_retention = [
      b
      for b in buckets or ()
      if b["retention_days"] > INCLUDED_RETENTION_DAYS
      and b["bucket_id"] not in IMMUTABLE_RETENTION_BUCKETS
  ]
  if over_retention:
    add(
        "over_retention",
        "Buckets retaining logs beyond the included 30 days",
        "Buckets exceed the 30 days of retention included with ingestion: "
        + ", ".join(
            f"{b['bucket_id']} ({b['retention_days']}d)" for b in over_retention
        )
        + ". Per-bucket stored volume is not exposed by the metrics used"
        " here, so no savings are claimed.",
        manual_step=(
            "Reduce bucket retention to the 30 days included with ingestion"
            " (google_logging_project_bucket_config.retention_days)."
        ),
        counted=False,
        flag=messages.FLAG_NOT_QUANTIFIED,
    )

  # --- Stale exclusion: the rule's target stream moved -----------------------
  for exclusion in exclusions or ():
    if exclusion.get("disabled"):
      continue
    name = str(exclusion.get("name") or "exclusion")
    for log_id in _log_ids_in_filter(str(exclusion.get("filter") or "")):
      target_bytes = bytes_by_log.get(log_id, 0.0)
      if target_bytes / total_stream_bytes > _DEAD_RULE_MAX_SHARE:
        continue  # Rule is still doing its job.

      # Dead rule: a successor stream with the same suffix is the target.
      successors = {
          other: other_bytes
          for other, other_bytes in bytes_by_log.items()
          if other != log_id
          and not is_data_access(other)
          and _stream_suffix(other) == _stream_suffix(log_id)
          and other_bytes / total_stream_bytes > _DEAD_RULE_MAX_SHARE
      }
      stale_claims = [
          (other, ALL_SEVERITIES, other_bytes * ledger.claim(other, 1.0))
          for other, other_bytes in successors.items()
      ]
      if not any(b > 0 for _, _, b in stale_claims):
        continue
      add(
          f"stale_exclusion_intent::{_stream_suffix(log_id)}",
          f"Exclusion '{name}' no longer matches its target stream",
          f"Exclusion '{name}' targets LOG_ID(\"{log_id}\"), which now"
          f" carries only {monthly(target_bytes):.2f} GiB/mo. The equivalent"
          f" stream {', '.join(successors)} carries"
          f" {monthly(sum(successors.values())):.2f} GiB/mo and is matched by"
          " no exclusion. The documented intent was to drop this volume.",
          stale_claims,
          confidence="medium",
          flag=messages.FLAG_INTENT_INFERRED,
      )

  # --- VPC flow logs sampled above the vendor default ------------------------
  enabled = [
      c
      for c in flow_log_configs or ()
      if str(c.get("state", "")).upper() == "ENABLED"
  ]
  samplings = [
      float(c["flow_sampling"]) for c in enabled if c.get("flow_sampling")
  ]
  # The least-sampled config bounds what every config would shed. Volume per
  # config is unknown, so anything higher could claim bytes that stay.
  floor_sampling = min(samplings) if samplings else 0.0
  if floor_sampling > FLOW_LOG_TARGET_SAMPLING:
    reduction = 1.0 - FLOW_LOG_TARGET_SAMPLING / floor_sampling
    flow_claims = [
        (log_id, ALL_SEVERITIES, num_bytes * ledger.claim(log_id, reduction))
        for log_id, num_bytes in bytes_by_log.items()
        if _stream_suffix(log_id) == "vpc_flows"
    ]
    if any(b > 0 for _, _, b in flow_claims):
      add(
          "flow_log_oversampling",
          "VPC flow logs sampled above the GCP default",
          f"All {len(samplings)} enabled flow log configs with a known rate"
          f" sample at {floor_sampling:.2f} or more, against the GCP console"
          f" default of {FLOW_LOG_TARGET_SAMPLING}. Flows are still captured,"
          " at lower fidelity.",
          flow_claims,
          manual_step=(
              f"Set flow_sampling to the {FLOW_LOG_TARGET_SAMPLING} console"
              " default on the VPC flow log configs"
              " (google_compute_subnetwork.log_config.flow_sampling, or the"
              " Network Management vpcFlowLogsConfigs API)."
          ),
          confidence="medium",
      )

  # --- DEBUG severity in production ------------------------------------------
  debug_claims = []
  for (log_id, severity), num_bytes in billable_streams.items():
    if severity.upper() != "DEBUG" or is_data_access(log_id):
      continue
    stream_total = bytes_by_log[log_id]
    granted = ledger.claim(log_id, num_bytes / stream_total)
    debug_claims.append((log_id, severity, stream_total * granted))
  debug_bytes = sum(b for _, _, b in debug_claims)
  if debug_bytes > 0:
    add(
        "debug_severity",
        "DEBUG severity logs retained in production",
        f"{monthly(debug_bytes):.2f} GiB/mo of DEBUG logs across"
        f" {sum(1 for _, _, b in debug_claims if b > 0)} stream(s).",
        debug_claims,
    )

  # --- Data Access audit logs: reported, never offered -----------------------
  # Measured against what stays billed: a duplicate copy is counted once, by
  # the duplicate-routing lever.
  audit_claims = [
      (log_id, severity, v * ledger.retained(log_id))
      for (log_id, severity), v in billable_streams.items()
      if is_data_access(log_id)
  ]
  audit_bytes = sum(b for _, _, b in audit_claims)
  if audit_bytes > 0:
    add(
        "data_access_audit_logs",
        "Data Access audit logs",
        f"{monthly(audit_bytes):.2f} GiB/mo of Data Access audit logs.",
        audit_claims,
        withheld=messages.WITHHELD_DATA_ACCESS.format(gib=monthly(audit_bytes)),
        counted=False,
    )

  counted = [a for a in levers if a.counted]
  total_pct = round(sum(a.pct_of_billable for a in counted), 2)
  return {
      "status": "ok",
      "basis": {
          "window_days": window_days,
          "source": "billing/bytes_ingested + byte_count (Cloud Monitoring)",
          "byte_count_to_billed_calibration": round(calibration, 4),
          # Both sides of the calibration ratio, so Prove It can re-derive it.
          "calibration_anchor": (
              "billing_export"
              if billed_window_gib is not None and billed_window_gib > 0
              else "billing/bytes_ingested"
          ),
          "anchor_window_gib": round(billed_total / BYTES_PER_GIB, 2),
          "byte_count_window_gib": round(raw_stream_total / BYTES_PER_GIB, 2),
          "baseline_monthly_gib": round(monthly_gib, 2),
          "billable_monthly_gib": round(billable_monthly_gib, 2),
          "billable_monthly_cost_usd": price_book.baseline_cost,
      },
      # The sum of the counted actions in `reduction_actions`.
      "headline": {
          "pct_of_billable_spend": total_pct,
          "monthly_savings_usd": round(sum(a.monthly_usd for a in counted), 2),
          "monthly_savings_gib": round(sum(a.monthly_gib for a in counted), 2),
          "exceeds_sanity_ceiling": total_pct > WASTE_SANITY_CEILING_PCT,
      },
      "uncounted_total_pct": round(
          sum(a.pct_of_billable or 0.0 for a in levers if not a.counted), 2
      ),
  }, levers
