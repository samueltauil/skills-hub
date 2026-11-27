"""One typed representation of a cost reduction action, and the ranked list.

`waste` builds lever actions (measured against billing metrics) and
`merge_actions` adds the sampled exclusion rules from `exclusion_rules`. Every
action carries what the report and Prove It need (`gib_by_sku`,
`stream_fraction`, `counted`, `flag`), so no consumer joins actions back to
anything by id or filter.
"""

import dataclasses
import hashlib
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

from constants import BYTES_PER_GIB
from constants import HOST_AUDIT_CAVEAT
from constants import HOST_AUDIT_PAYLOAD_MARKERS
from constants import SECURITY_TELEMETRY_LOG_IDS
from exclusion_rules import decode_log_id
from exclusion_rules import log_name_predicate
from exclusion_rules import rule_eligibility
from exclusion_rules import severity_predicate
import messages
from pricing import PriceBook

SOURCE_LEVER = "measured_lever"
SOURCE_RULE = "exclusion_rule"
ALL_SEVERITIES = "*"

# Cloud Logging rejects exclusion filters longer than this.
MAX_FILTER_CHARS = 20000
# Whole-stream filters stop below the first severity `rule_eligibility` refuses
# (`NEVER_EXCLUDE_SEVERITIES`), so they never drop a paging signal.
_WHOLE_STREAM_GUARD = "severity < CRITICAL"


@dataclasses.dataclass(frozen=True)
class Claim:
  """A stream (at one severity, or every severity) an action's volume covers."""

  log_id: str
  severity: str
  monthly_gib: float

  def to_dict(self) -> Dict[str, Any]:
    return {
        "log_id": self.log_id,
        "severity": self.severity,
        "monthly_gib": round(self.monthly_gib, 3),
    }

  def covers(self, other: "Claim") -> bool:
    """True when every byte of `other` falls in this stream and severity."""
    return decode_log_id(self.log_id) == decode_log_id(other.log_id) and (
        self.severity in (ALL_SEVERITIES, other.severity)
    )


@dataclasses.dataclass
class Action:
  """One saving the reader can act on, or a reason it is withheld."""

  id: str
  title: str
  source: str
  evidence: str
  # In the recoverable-spend floor; the headline is the sum of these.
  counted: bool = False
  # None when the volume behind the action is not measurable.
  monthly_gib: Optional[float] = None
  monthly_usd: Optional[float] = None
  pct_of_billable: Optional[float] = None
  gib_by_sku: Dict[str, float] = dataclasses.field(default_factory=dict)
  # Share of the claimed streams' bytes the action removes, for re-measuring.
  stream_fraction: float = 1.0
  claims: List[Claim] = dataclasses.field(default_factory=list)
  refused_claims: List[Dict[str, Any]] = dataclasses.field(default_factory=list)
  filter: str = ""
  manual_step: str = ""
  scope_note: str = ""
  sample_log: Optional[Dict[str, Any]] = None
  # Reader-facing sentence; what the reader must decide before acting.
  flag: str = ""
  confidence: str = "high"
  # Rules only: share of the sampled volume the filter matches.
  projected_savings_pct: Optional[float] = None
  rule_scope: str = ""
  # Set when the action is reported but never offered.
  withheld: str = ""

  def covers(self, claim: Claim) -> bool:
    return any(c.covers(claim) for c in self.claims)

  def assurance(self) -> Dict[str, str]:
    """The plain-language verdict on how far to trust this action."""
    sample = _sample_text(self.sample_log)
    if self.source == SOURCE_RULE:
      return _verdict(
          "estimated",
          measurement=[messages.HOW_MEASURED_RULE],
          judgement=[
              messages.SCOPE_JUDGEMENT.get(
                  self.rule_scope, messages.SCOPE_JUDGEMENT["signature"]
              )
              + (messages.READ_SAMPLE if sample else "")
          ],
          caveat=_security_caveat(
              (c.log_id for c in self.claims), sample, drops_stream=True
          ),
      )
    quantified = self.monthly_gib is not None
    if not quantified:
      level = "unmeasured"
    elif not self.counted:
      level = "judgement"
    elif self.flag or self.confidence != "high":
      level = "confirm"
    else:
      level = "ready"
    return _verdict(
        level,
        measurement=[messages.HOW_MEASURED_LEVER if quantified else ""],
        judgement=[
            self.flag,
            messages.CONFIDENCE_MEANINGS.get(self.confidence, ""),
        ],
        # Includes refused claims: they still signal security telemetry.
        caveat=_security_caveat(
            [c.log_id for c in self.claims]
            + [r["log_id"] for r in self.refused_claims],
            sample,
            drops_stream=bool(self.filter),
        ),
    )

  def to_dict(self) -> Dict[str, Any]:
    return {
        "id": self.id,
        "title": self.title,
        "source": self.source,
        "counted": self.counted,
        "flag": self.flag,
        "monthly_gib": self.monthly_gib,
        "monthly_usd": self.monthly_usd,
        "pct_of_billable": self.pct_of_billable,
        "gib_by_sku": self.gib_by_sku,
        "stream_fraction": self.stream_fraction,
        "projected_savings_pct": self.projected_savings_pct,
        "claims": [c.to_dict() for c in self.claims],
        "refused_claims": self.refused_claims,
        "evidence": self.evidence,
        "filter": self.filter,
        "manual_step": self.manual_step,
        "scope_note": self.scope_note,
        "sample_log": self.sample_log,
        "assurance": self.assurance(),
    }


# --- Assurance ---------------------------------------------------------------


def _sample_text(sample: Optional[Mapping[str, Any]]) -> str:
  """The example log text the report would render, or ""."""
  sample = sample or {}
  return str(sample.get("payload") or sample.get("preview") or "")


def _join_prose(items: Sequence[str]) -> str:
  if len(items) <= 1:
    return "".join(items)
  return f"{', '.join(items[:-1])} and {items[-1]}"


def _security_caveat(
    log_ids: Iterable[str], sample_text: str, drops_stream: bool
) -> str:
  """Returns a caveat if the streams are security telemetry, else ""."""
  # GCP security streams are matched by log ID; host audit streams by sample
  # text. `drops_stream` is False when the action only reduces a stream (e.g.
  # sampling).
  described = sorted({
      SECURITY_TELEMETRY_LOG_IDS[decoded]
      for decoded in map(decode_log_id, log_ids)
      if decoded in SECURITY_TELEMETRY_LOG_IDS
  })
  if not described and any(
      m in sample_text for m in HOST_AUDIT_PAYLOAD_MARKERS
  ):
    described = [HOST_AUDIT_CAVEAT]
  if not described:
    return ""
  template = (
      messages.SECURITY_CAVEAT_DROPS
      if drops_stream
      else messages.SECURITY_CAVEAT_REDUCES
  )
  return template.format(what=_join_prose(described))


def _verdict(
    level: str,
    measurement: Sequence[str],
    judgement: Sequence[str],
    caveat: str,
) -> Dict[str, str]:
  # "Ready to apply" is never the word for deleting security telemetry.
  if caveat and level == "ready":
    level = "confirm"
  return {
      "level": level,
      "label": messages.LEVEL_LABELS[level],
      "measurement": " ".join(s for s in measurement if s),
      "judgement": " ".join(s for s in judgement if s),
      "caveat": caveat,
  }


# --- Filters -----------------------------------------------------------------


def _render_filter(claims: Sequence[Claim], project_id: str) -> str:
  """Renders claims as one filter, one OR-group per severity."""
  by_severity: Dict[str, List[str]] = {}
  for claim in claims:
    by_severity.setdefault(claim.severity, []).append(
        log_name_predicate(project_id, claim.log_id)
    )

  groups = []
  for severity, log_preds in by_severity.items():
    if severity == ALL_SEVERITIES:
      severity_pred = _WHOLE_STREAM_GUARD
    else:
      severity_pred = severity_predicate(severity)
    logs = (
        log_preds[0] if len(log_preds) == 1 else f"({' OR '.join(log_preds)})"
    )
    groups.append(f"{severity_pred} AND {logs}")
  if len(groups) == 1:
    return groups[0]
  return " OR ".join(f"({g})" for g in groups)


def _refusal_reason(claim: Claim) -> Optional[str]:
  if not claim.log_id or claim.log_id == "unknown":
    return messages.REFUSED_NO_LOG_ID
  ok, reason = rule_eligibility(
      severity="" if claim.severity == ALL_SEVERITIES else claim.severity,
      log_id=claim.log_id,
      rule_bytes=int(claim.monthly_gib * BYTES_PER_GIB),
  )
  return None if ok else reason


def filter_from_claims(
    claims: Sequence[Claim], project_id: str
) -> Tuple[str, List[Claim], List[Dict[str, Any]]]:
  """Builds a copy-paste filter covering the claims it can safely exclude.

  Args:
    claims: candidate claims to exclude.
    project_id: project the filter targets.

  Returns:
    `(filter, kept, refused)`; `refused` entries carry a reason and the
    filter is "" when nothing is kept.
  """
  kept: List[Claim] = []
  refused: List[Dict[str, Any]] = []
  for claim in sorted(claims, key=lambda c: c.monthly_gib, reverse=True):
    reason = _refusal_reason(claim)
    if reason is None and (
        len(_render_filter([*kept, claim], project_id)) > MAX_FILTER_CHARS
    ):
      reason = messages.REFUSED_FILTER_TOO_LONG.format(limit=MAX_FILTER_CHARS)
    if reason is not None:
      refused.append({**claim.to_dict(), "reason": reason})
    else:
      kept.append(claim)
  return (_render_filter(kept, project_id) if kept else ""), kept, refused


# --- Exclusion rules ---------------------------------------------------------


def _rule_action(raw: Mapping[str, Any], price_book: PriceBook) -> Action:
  """Converts one `exclusion_rules` candidate into an action."""
  log_id = raw["log_id"]
  severity = raw["severity"]
  gib = raw["projected_savings_gib"]
  scope = raw["rule_scope"]
  # Several rules can share a stream and severity (two signatures, or two
  # resource types), so the filter is part of the identity.
  digest = hashlib.sha1(raw["filter"].encode("utf-8")).hexdigest()[:8]
  return Action(
      id=f"exclusion::{log_id}::{severity}::{digest}",
      title=raw["title"],
      source=SOURCE_RULE,
      evidence=raw["rationale"],
      monthly_gib=gib,
      monthly_usd=raw["projected_monthly_savings_usd"],
      gib_by_sku={price_book.sku_for_log(log_id): gib},
      claims=[Claim(log_id, severity, gib)],
      filter=raw["filter"],
      # A stream-scoped rule's reach is already stated in its judgement.
      scope_note=raw["rule_scope_note"] if scope == "signature" else "",
      sample_log=raw["sample_log"] or None,
      projected_savings_pct=raw["projected_savings_pct"],
      rule_scope=scope,
  )


def merge_actions(
    lever_actions: Sequence[Action],
    exclusion_candidates: Sequence[Mapping[str, Any]],
    price_book: PriceBook,
) -> Dict[str, Any]:
  """Builds the `reduction_actions` contract: ranked actions and withheld.

  A rule whose stream a lever's filter already covers folds into that lever
  (lending it its example log); a rule beside a manual-step lever on the same
  stream stays, marked as an alternative; exact duplicate filters are dropped.

  Args:
    lever_actions: actions from `waste.compute_extraneous_spend`.
    exclusion_candidates: raw candidates from `exclusion_rules`.
    price_book: prices the candidates.

  Returns:
    The `reduction_actions` dict.
  """
  actions: List[Action] = []
  withheld: List[Dict[str, str]] = []
  for action in lever_actions:
    if action.withheld:
      withheld.append({"title": action.title, "reason": action.withheld})
    else:
      actions.append(action)
  levers = list(actions)
  filters = {a.filter for a in levers if a.filter}

  for raw in exclusion_candidates:
    rule = _rule_action(raw, price_book)
    if rule.monthly_gib <= 0:
      withheld.append(
          {"title": rule.title, "reason": messages.WITHHELD_NO_VOLUME}
      )
      continue
    if rule.filter in filters:
      continue
    claim = rule.claims[0]
    covering = next((a for a in levers if a.filter and a.covers(claim)), None)
    if covering is not None:
      covering.sample_log = covering.sample_log or rule.sample_log
      continue
    beside = next(
        (a for a in levers if a.manual_step and a.covers(claim)), None
    )
    if beside is not None:
      rule.scope_note = " ".join(
          filter(
              None,
              [
                  rule.scope_note,
                  messages.ALTERNATIVE_TO.format(title=beside.title),
              ],
          )
      )
    filters.add(rule.filter)
    actions.append(rule)

  # Dollars first: SKU rates differ, so largest volume != largest saving.
  actions.sort(
      key=lambda a: (a.monthly_usd or 0.0, a.monthly_gib or 0.0), reverse=True
  )
  return {"actions": [a.to_dict() for a in actions], "withheld": withheld}
