"""Builds precise, verifiable Cloud Logging exclusion filters.

Exclusions are irreversible, so these helpers guard against over-broad rules
(drop needed logs) first and no-op rules (match nothing) second.
"""

import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple
import urllib.parse

from constants import BYTES_PER_GIB
from constants import DATA_ACCESS_LOG_IDS
from constants import FREE_REQUIRED_LOG_IDS
from constants import MASK_PLACEHOLDERS
from constants import MAX_EXCLUSION_CANDIDATES
from constants import SIGNATURE_TEMPLATE_CHARS
from pricing import PriceBook

# Maps the Log Analytics `signature_source` marker onto the Cloud Logging
# filter field holding the same value.
SIGNATURE_SOURCE_FIELDS = {
    "text_payload": "textPayload",
    "json_message": "jsonPayload.message",
    "json_MESSAGE": "jsonPayload.MESSAGE",
    "json_msg": "jsonPayload.msg",
    "json_log": "jsonPayload.log",
    "audit_method": "protoPayload.methodName",
}

# 'proto_type' (`@type`) is not reliably addressable in a filter, and
# 'json_shape' is a synthesised key skeleton no filter can select, so both
# stay stream-scoped.

# A signature must recur this many times in the sample window before it is
# treated as a durable pattern worth targeting.
MIN_SIGNATURE_ENTRIES = 10

# Shorter prefixes are not specific enough to bound the blast radius.
MIN_PREFIX_CHARS = 16

# Same length as the SQL grouping prefix, so an anchored prefix matches
# exactly the rows in the group.
MAX_PREFIX_CHARS = SIGNATURE_TEMPLATE_CHARS

# Severities that page a human; excluding them risks a missed incident.
NEVER_EXCLUDE_SEVERITIES = ("CRITICAL", "ALERT", "EMERGENCY")


def decode_log_id(log_id: str) -> str:
  """Returns `log_id` decoded; `logName` stores IDs percent-encoded."""
  return urllib.parse.unquote(log_id or "")


_FREE_REQUIRED = frozenset(
    decode_log_id(i).lower() for i in FREE_REQUIRED_LOG_IDS
)
_DATA_ACCESS = frozenset(decode_log_id(i).lower() for i in DATA_ACCESS_LOG_IDS)


def is_free_required(log_id: str) -> bool:
  """True for `_Required` streams, which are billed at $0."""
  return decode_log_id(log_id).lower() in _FREE_REQUIRED


def is_data_access(log_id: str) -> bool:
  """True for Data Access audit streams, which are never offered as savings."""
  return decode_log_id(log_id).lower() in _DATA_ACCESS


_CONTROL_CHARS = re.compile(r"[\x00-\x1f\x7f-\x9f]")

# Built from the same tuple the SQL masks with, so the two stay in sync.
_MASK_PLACEHOLDER = re.compile(
    "|".join(re.escape(token) for token in MASK_PLACEHOLDERS)
)

# Tokens that rotate between otherwise identical lines; a prefix containing
# one stops matching once the value changes.
_VOLATILE_TOKEN = re.compile(
    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"  # uuid
    r"|\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"  # ipv4
    r"|\b[0-9a-f]{16,}\b"  # trace / hash
    r"|\b\d{4,}\b"  # epoch, port, counter, numeric id
    r"|\d{2}:\d{2}:\d{2}",  # clock time
    re.IGNORECASE,
)

_RE2_METACHARS = re.compile(r"([\\.^$|()\[\]{}*+?])")


def escape_filter_string(value: str) -> str:
  """Escapes a value for embedding in a double-quoted filter string literal."""
  # Only `"` is escaped: the filter parser passes backslashes through verbatim,
  # so a regex escape needs a single backslash (`\.`, not `\\.`).
  return (value or "").replace('"', '\\"')


def escape_re2_literal(value: str) -> str:
  """Escapes RE2 metacharacters so `value` matches only itself."""
  # Narrower than `re.escape`, whose escapes of e.g. space are not portable RE2.
  return _RE2_METACHARS.sub(r"\\\1", value or "")


def encode_log_id(log_id: str) -> str:
  """Percent-encodes a log ID the way it appears inside `logName`."""
  # Unquotes first so already-encoded IDs are not double-encoded.
  if not log_id:
    return ""
  return urllib.parse.quote(decode_log_id(log_id), safe="")


def severity_predicate(severity: str) -> str:
  # DEFAULT included: omitting the predicate matches every severity.
  return f'severity = "{escape_filter_string(severity)}"'


def log_name_predicate(project_id: str, log_id: str) -> str:
  return (
      f'logName = "projects/{escape_filter_string(project_id)}/logs/'
      f'{escape_filter_string(encode_log_id(log_id))}"'
  )


def narrow_predicate(
    signature_source: Optional[str],
    signature_prefix: Optional[str],
    entry_count: int = 0,
) -> Tuple[Optional[str], Optional[str]]:
  """Returns `(predicate, None)` matching one signature, or `(None, reason)`."""
  field = SIGNATURE_SOURCE_FIELDS.get(signature_source or "")
  if not field:
    return None, "signature field is not addressable in a log filter"

  text = signature_prefix or ""
  if not text.strip():
    return None, "no signature text was captured"
  # A masked template ('<N>') would be matched literally by RE2 and find
  # nothing; only unmasked signatures can be narrowed.
  if _MASK_PLACEHOLDER.search(text):
    return None, (
        "signature is a normalised template; its variable tokens cannot be"
        " matched literally"
    )
  if _CONTROL_CHARS.search(text):
    return None, "signature contains control characters"
  if len(text) < MIN_PREFIX_CHARS:
    return None, "signature is too short to bound the match"
  if _VOLATILE_TOKEN.search(text):
    return None, "signature embeds a rotating id, address or timestamp"
  if (entry_count or 0) < MIN_SIGNATURE_ENTRIES:
    return None, (
        f"pattern recurred fewer than {MIN_SIGNATURE_ENTRIES} times in the"
        " sample window"
    )

  pattern = "^" + escape_re2_literal(text[:MAX_PREFIX_CHARS])
  return f'{field} =~ "{escape_filter_string(pattern)}"', None


def rule_eligibility(
    severity: str,
    log_id: str = "",
    rule_bytes: int = 0,
    rule_entries: int = 0,
) -> Tuple[bool, Optional[str]]:
  """Returns `(eligible, reason)`: is the rule safe and worth recommending?"""
  # Any failure disqualifies the rule outright.
  if (severity or "").upper() in NEVER_EXCLUDE_SEVERITIES:
    return False, (
        f"{severity} entries page an on-call; excluding them trades an"
        " incident signal for negligible savings"
    )

  if is_free_required(log_id):
    return False, (
        "_Required stream, already billed at $0; excluding it saves nothing"
        " and may breach audit retention obligations"
    )

  if is_data_access(log_id):
    return False, (
        "Data Access audit logs; these may be required by your organisation's"
        " audit obligations, so they are reported but never counted as"
        " recoverable spend"
    )

  if not (rule_bytes > 0 or rule_entries > 0):
    return False, "no volume measured in the sample window; savings unknown"

  return True, None


def build_sample_rule(
    sig: Mapping[str, Any], project_id: str
) -> Dict[str, Any]:
  """Builds an exclusion rule for one signature row, with the volume it drops.

  Narrowed to the signature when its text is safely matchable, else widened to
  the whole stream at that severity. Not priced here: sample bytes are Log
  Analytics payload bytes, so the caller anchors savings to the billed run
  rate.

  Args:
    sig: one row from `analytics` signature output.
    project_id: project the filter targets.

  Returns:
    The rule's filter, scope, measured volume and eligibility.
  """
  service, severity, log_id = sig["service"], sig["severity"], sig["log_id"]
  parts = [severity_predicate(severity)]
  if service != "unknown":
    parts.insert(0, f'resource.type = "{escape_filter_string(service)}"')
  if log_id != "unknown":
    parts.append(log_name_predicate(project_id, log_id))

  predicate, reason = narrow_predicate(
      sig["signature_source"], sig["preview"], sig["count"]
  )
  if predicate:
    parts.append(predicate)
    scope, note = "signature", "this pattern only"
    rule_bytes, rule_entries = sig["total_bytes"], sig["count"]
  else:
    scope, note = "stream", "entire stream at this severity"
    rule_bytes, rule_entries = (
        sig["stream_total_bytes"],
        sig["stream_entry_count"],
    )

  eligible, ineligible_reason = rule_eligibility(
      severity, log_id, rule_bytes, rule_entries
  )
  return {
      "filter": " AND ".join(parts),
      "rule_scope": scope,
      "rule_scope_note": note,
      "rule_scope_reason": reason,
      "rule_bytes": rule_bytes,
      "rule_entry_count": rule_entries,
      "eligible": eligible,
      "ineligible_reason": ineligible_reason,
  }


# A rule under both floors is not worth an owner's attention, and its estimate
# is dominated by sampling noise.
MIN_RULE_SHARE_PCT = 5.0
MIN_RULE_GIB = 50.0
MIN_RULE_ENTRIES = 50_000


def _title(rule: Mapping[str, Any], service: str, severity: str, log_id: str):
  where = f"{service} ({log_id})"
  if rule["rule_scope"] == "signature":
    return f"Exclude repetitive log pattern in {where}"
  if severity in ("DEBUG", "DEFAULT"):
    return f"Filter routine {severity} logs in {where}"
  if severity == "INFO":
    return f"Filter chatty INFO logs for {where}"
  return f"Filter {severity} logs in {where}"


def generate_exclusion_candidates(
    signatures: Sequence[Mapping[str, Any]],
    price_book: PriceBook,
    project_id: str,
    total_entries: int,
    total_sample_bytes: int,
    monthly_run_rate_gib: float,
    sample_days: float,
) -> List[Dict[str, Any]]:
  """Proposes Log Router exclusion rules, ranked by the volume each one drops.

  The only surface emitting copy-pasteable exclusions; every rule passes the
  `rule_eligibility` gates.

  Args:
    signatures: signature rows from the Log Analytics sample.
    price_book: prices each rule's savings.
    project_id: project the filters target.
    total_entries: entries in the sample.
    total_sample_bytes: bytes in the sample.
    monthly_run_rate_gib: billed monthly ingestion savings are anchored to.
    sample_days: length of the sample window.

  Returns:
    Candidate rules, largest first.
  """
  by_filter: Dict[str, Dict[str, Any]] = {}
  for sig in signatures:
    srv, sev, log_id = sig["service"], sig["severity"], sig["log_id"]
    rule = build_sample_rule(sig, project_id)
    if not rule["eligible"]:
      continue

    # Gate on what the rule drops, which for a widened rule is the whole
    # stream. The share basis is chosen per rule: a stream's byte column may
    # be NULL.
    rule_bytes, rule_entries = rule["rule_bytes"], rule["rule_entry_count"]
    if rule_bytes > 0 and total_sample_bytes > 0:
      pct = round(100.0 * rule_bytes / total_sample_bytes, 1)
      large = rule_bytes / BYTES_PER_GIB >= MIN_RULE_GIB
      magnitude = f"~{rule_bytes / BYTES_PER_GIB:,.1f} GiB"
    elif rule_entries > 0 and total_entries > 0:
      pct = round(100.0 * rule_entries / total_entries, 1)
      large = rule_entries >= MIN_RULE_ENTRIES
      magnitude = f"~{rule_entries:,} entries"
    else:
      continue
    if pct < MIN_RULE_SHARE_PCT and not large:
      continue

    filt = rule["filter"]
    prior = by_filter.get(filt)
    if prior is not None and rule_bytes <= prior["sample_bytes"]:
      continue

    scope_phrase = (
        rule["rule_scope_note"]
        if rule["rule_scope"] == "signature"
        else f"all {sev} logs in stream '{log_id}'"
    )
    rationale = (
        f"Drops {scope_phrase}: {magnitude} over the {sample_days:g}-day"
        f" sample ({pct}% of sampled volume)."
    )
    if rule["rule_scope_reason"]:
      rationale += f" Scoped to the stream because {rule['rule_scope_reason']}."

    # Apportion the billed run rate by the sampled share: payload bytes
    # overstate billed volume, so the sample is trusted only for the ratio.
    monthly_gib = pct / 100.0 * monthly_run_rate_gib
    by_filter[filt] = {
        "title": _title(rule, srv, sev, log_id),
        "service": srv,
        "severity": sev,
        "log_id": log_id,
        "filter": filt,
        "sample_bytes": rule_bytes,
        "rule_scope": rule["rule_scope"],
        "rule_scope_note": rule["rule_scope_note"],
        "projected_savings_pct": pct,
        "projected_savings_gib": round(monthly_gib, 2),
        # Difference of two bills, so the per-SKU free tier is respected.
        "projected_monthly_savings_usd": price_book.saving(
            {price_book.sku_for_log(log_id): monthly_gib}
        ),
        "rationale": rationale,
        "sample_log": sig["sample_log"],
    }

  ranked = sorted(
      by_filter.values(),
      key=lambda c: (c["sample_bytes"], c["projected_savings_pct"]),
      reverse=True,
  )
  # A stream rule subsumes signature rules on its stream; keeping both would
  # double count.
  streams = {
      (c["service"], c["severity"], c["log_id"])
      for c in ranked
      if c["rule_scope"] == "stream"
  }
  disjoint = [
      c
      for c in ranked
      if c["rule_scope"] == "stream"
      or (c["service"], c["severity"], c["log_id"]) not in streams
  ]
  return disjoint[:MAX_EXCLUSION_CANDIDATES]
