#!/usr/bin/env python3
"""Analyzes and validates matched DB resources against DBResourcesStore.

Validates every fw_id, cc_id, and selected_parameters entry in
CatalogMatchResult against DBResourcesStore, enforces built-in priority
guardrails (omitting underlying_ccs by default unless --include_underlying_ccs
is passed, mapping standalone CloudControls to the BUILT_IN Frameworks that
contain them, dropping standalone CloudControls that a selected Framework
already contains, computing whether a single BUILT_IN Framework covers all
additional CCs, and ignoring MINOR requirements not met by built-in Frameworks),
and outputs MatchAnalysisReport. The matched Frameworks are sorted from the best
to the weakest match, each with its match_percentage, and none is dropped for a
low percentage. Custom resources are suggested, and the hand-off for the author
skill (author_handoff.json) is written, only when the overall match is less than
80 percent or when additional CCs have no common BUILT_IN Framework.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import pathlib
import sys
from typing import Any, Literal

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import db_resources_loader  # pylint: disable=g-import-not-at-top

DBResourcesStore = db_resources_loader.DBResourcesStore

ANALYSIS_REPORT_FILE = "analysis_report.json"
AUTHOR_HANDOFF_FILE = "author_handoff.json"

# Custom Frameworks and CloudControls are suggested for unmet MAJOR requirements
# only when the overall match is less than this percentage. A built-in Framework
# is recommended whatever its own match percentage is.
CUSTOM_RESOURCES_MATCH_THRESHOLD = 80.0


@dataclasses.dataclass
class RequirementItem:
  """Single compliance or workload requirement extracted from user_prompt."""

  requirement: str
  importance: Literal["MAJOR", "MINOR"] = "MAJOR"
  compliance_regime_or_domain: str = ""
  target_service: str | None = None
  target_resource_type: str | None = None
  desired_constraint: dict[str, Any] = dataclasses.field(default_factory=dict)
  suggested_custom_cc_summary: str = ""

  @classmethod
  def from_dict(cls, data: dict[str, Any]) -> RequirementItem:
    """Constructs a RequirementItem from a dictionary."""
    req_text = data.get("requirement") or data.get("description") or ""
    raw_importance = str(data.get("importance", "MAJOR")).upper()
    importance: Literal["MAJOR", "MINOR"] = (
        "MINOR" if raw_importance == "MINOR" else "MAJOR"
    )
    return cls(
        requirement=str(req_text),
        importance=importance,
        compliance_regime_or_domain=str(
            data.get("compliance_regime_or_domain", "")
        ),
        target_service=data.get("target_service"),
        target_resource_type=data.get("target_resource_type"),
        desired_constraint=dict(data.get("desired_constraint", {})),
        suggested_custom_cc_summary=str(
            data.get("suggested_custom_cc_summary", "")
        ),
    )


@dataclasses.dataclass
class NavigatorIntentSpec:
  """Normalized intent specification derived from user_prompt."""

  source_type: Literal["DIRECT_NL"]
  organization_id: str | None
  user_prompt: str
  compliance_regimes: list[str] = dataclasses.field(default_factory=list)
  allowed_locations: list[str] = dataclasses.field(default_factory=list)
  target_services: list[str] = dataclasses.field(default_factory=list)
  requirements: list[RequirementItem] = dataclasses.field(default_factory=list)

  @classmethod
  def from_dict(cls, data: dict[str, Any]) -> NavigatorIntentSpec:
    """Constructs a NavigatorIntentSpec from a dictionary."""
    return cls(
        source_type=data["source_type"],
        organization_id=data.get("organization_id"),
        user_prompt=str(data.get("user_prompt", "")),
        compliance_regimes=list(data.get("compliance_regimes", [])),
        allowed_locations=list(data.get("allowed_locations", [])),
        target_services=list(data.get("target_services", [])),
        requirements=[
            RequirementItem.from_dict(r) for r in data.get("requirements", [])
        ],
    )


@dataclasses.dataclass
class ParentFrameworkRef:
  """Reference to a BUILT_IN Framework that includes a CloudControl."""

  fw_id: str
  display_name: str

  @classmethod
  def from_dict(cls, data: dict[str, Any]) -> ParentFrameworkRef:
    """Constructs a ParentFrameworkRef from a dictionary."""
    fw_id = str(data["fw_id"])
    return cls(
        fw_id=fw_id,
        display_name=str(data.get("display_name", fw_id)),
    )


@dataclasses.dataclass
class MatchedCC:
  """CloudControl matched or populated from a Framework."""

  cc_id: str
  cc_type: Literal["BUILT_IN", "CUSTOM"]
  display_name: str
  requirement: str = ""
  importance: Literal["MAJOR", "MINOR"] = "MAJOR"
  match_rationale: str = ""
  part_of_builtin_frameworks: list[ParentFrameworkRef] = dataclasses.field(
      default_factory=list
  )
  matched_rule_types: list[str] = dataclasses.field(default_factory=list)
  selected_parameters: dict[str, Any] = dataclasses.field(default_factory=dict)

  @classmethod
  def from_dict(cls, data: dict[str, Any]) -> MatchedCC:
    """Constructs a MatchedCC from a dictionary."""
    cc_id = str(data["cc_id"])
    default_type = "BUILT_IN" if cc_id.startswith("builtin-") else "CUSTOM"
    raw_importance = str(data.get("importance", "MAJOR")).upper()
    importance: Literal["MAJOR", "MINOR"] = (
        "MINOR" if raw_importance == "MINOR" else "MAJOR"
    )
    return cls(
        cc_id=cc_id,
        cc_type=data.get("cc_type", default_type),
        display_name=str(data.get("display_name", cc_id)),
        requirement=str(data.get("requirement", "")),
        importance=importance,
        match_rationale=str(data.get("match_rationale", "")),
        part_of_builtin_frameworks=[
            ParentFrameworkRef.from_dict(f)
            for f in data.get("part_of_builtin_frameworks", [])
        ],
        matched_rule_types=list(data.get("matched_rule_types", [])),
        selected_parameters=dict(data.get("selected_parameters", {})),
    )


@dataclasses.dataclass
class MatchedFW:
  """Framework matched against requirements."""

  fw_id: str
  fw_type: Literal["BUILT_IN", "CUSTOM"]
  major_revision_id: int
  display_name: str
  match_rationale: str = ""
  satisfied_requirements: list[str] = dataclasses.field(default_factory=list)
  # The percentage of the MAJOR requirements of the intent that this Framework
  # satisfies. The analyzer computes it; a value in the input is ignored.
  match_percentage: float = 0.0
  underlying_ccs: list[MatchedCC] | None = None

  @classmethod
  def from_dict(cls, data: dict[str, Any]) -> MatchedFW:
    """Constructs a MatchedFW from a dictionary."""
    fw_id = str(data["fw_id"])
    default_type = "BUILT_IN" if fw_id.startswith("builtin-") else "CUSTOM"
    raw_underlying = data.get("underlying_ccs")
    return cls(
        fw_id=fw_id,
        fw_type=data.get("fw_type", default_type),
        major_revision_id=int(data.get("major_revision_id", 1)),
        display_name=str(data.get("display_name", fw_id)),
        match_rationale=str(data.get("match_rationale", "")),
        satisfied_requirements=list(data.get("satisfied_requirements", [])),
        underlying_ccs=(
            [MatchedCC.from_dict(c) for c in raw_underlying]
            if raw_underlying is not None
            else None
        ),
    )


@dataclasses.dataclass
class CatalogMatchResult:
  """Candidate match output before deterministic verification."""

  selected_frameworks: list[MatchedFW] = dataclasses.field(default_factory=list)
  standalone_matched_ccs: list[MatchedCC] = dataclasses.field(
      default_factory=list
  )
  unmatched_requirements: list[RequirementItem] = dataclasses.field(
      default_factory=list
  )

  @classmethod
  def from_dict(cls, data: dict[str, Any]) -> CatalogMatchResult:
    """Constructs a CatalogMatchResult from a dictionary."""
    return cls(
        selected_frameworks=[
            MatchedFW.from_dict(f) for f in data.get("selected_frameworks", [])
        ],
        standalone_matched_ccs=[
            MatchedCC.from_dict(c)
            for c in data.get("standalone_matched_ccs", [])
        ],
        unmatched_requirements=[
            RequirementItem.from_dict(r)
            for r in data.get("unmatched_requirements", [])
        ],
    )


@dataclasses.dataclass
class MatchAnalysisReport:
  """High-level verified match analysis report."""

  matched_frameworks: list[MatchedFW] = dataclasses.field(default_factory=list)
  additional_cloud_controls: list[MatchedCC] = dataclasses.field(
      default_factory=list
  )
  common_builtin_frameworks_for_additional_ccs: list[ParentFrameworkRef] = (
      dataclasses.field(default_factory=list)
  )
  suggest_custom_framework_for_additional_ccs: bool = False
  unmet_major_requirements: list[RequirementItem] = dataclasses.field(
      default_factory=list
  )
  match_score_percentage: float = 100.0
  suggest_custom_resources_for_unmet_requirements: bool = False
  custom_authoring_handoff: dict[str, Any] | None = None
  location: str = db_resources_loader.DEFAULT_LOCATION

  def to_dict(self) -> dict[str, Any]:
    """Serializes report to dict, omitting underlying_ccs when None."""
    payload = dataclasses.asdict(self)
    for fw_dict in payload.get("matched_frameworks", []):
      if fw_dict.get("underlying_ccs") is None:
        fw_dict.pop("underlying_ccs", None)
    return payload


def _infer_resource_type(
    raw_item: dict[str, Any], resource_id: str
) -> Literal["BUILT_IN", "CUSTOM"]:
  """Infers BUILT_IN vs CUSTOM from proto JSON or ID prefix."""
  explicit = raw_item.get("type")
  if explicit in ("BUILT_IN", "CUSTOM"):
    return explicit
  return "BUILT_IN" if resource_id.startswith("builtin-") else "CUSTOM"


def _extract_rule_types(raw_cc: dict[str, Any]) -> list[str]:
  """Extracts rule implementation keys and action types from a CloudControl."""
  extracted: list[str] = []
  ignored_keys = {"description", "ruleActionTypes"}
  for rule in raw_cc.get("rules", []):
    if not isinstance(rule, dict):
      continue
    for key in rule:
      if key not in ignored_keys and key not in extracted:
        extracted.append(key)
    for action_type in rule.get("ruleActionTypes", []):
      if action_type not in extracted:
        extracted.append(action_type)
  return extracted


def _framework_cc_ids(raw_fw: dict[str, Any]) -> set[str]:
  """Returns the IDs of the CloudControls that a Framework contains."""
  return {
      detail.get("name", "").split("/")[-1]
      for detail in raw_fw.get("cloudControlDetails", [])
      if isinstance(detail, dict) and detail.get("name")
  }


def _resolve_parent_builtin_frameworks(
    cc_id: str,
    raw_cc: dict[str, Any],
    resources: DBResourcesStore,
) -> list[ParentFrameworkRef]:
  """Finds all BUILT_IN Frameworks in DBResourcesStore that include cc_id."""
  parent_fw_ids: set[str] = set()
  for related_fw in raw_cc.get("relatedFrameworks", []):
    if isinstance(related_fw, str) and related_fw in resources.frameworks:
      raw_related = resources.frameworks[related_fw]
      if _infer_resource_type(raw_related, related_fw) == "BUILT_IN":
        parent_fw_ids.add(related_fw)

  for fw_id, raw_fw in resources.frameworks.items():
    if _infer_resource_type(raw_fw, fw_id) != "BUILT_IN":
      continue
    for detail in raw_fw.get("cloudControlDetails", []):
      if not isinstance(detail, dict):
        continue
      detail_cc_id = detail.get("name", "").split("/")[-1]
      if detail_cc_id == cc_id:
        parent_fw_ids.add(fw_id)
        break

  return [
      ParentFrameworkRef(
          fw_id=fid,
          display_name=resources.frameworks[fid].get("displayName", fid),
      )
      for fid in sorted(parent_fw_ids)
  ]


def _compute_common_parent_frameworks(
    standalone_ccs: list[MatchedCC],
) -> list[ParentFrameworkRef]:
  """Computes BUILT_IN Frameworks that contain all standalone_ccs."""
  if not standalone_ccs:
    return []
  common_ids = {
      ref.fw_id for ref in standalone_ccs[0].part_of_builtin_frameworks
  }
  display_by_id = {
      ref.fw_id: ref.display_name
      for ref in standalone_ccs[0].part_of_builtin_frameworks
  }
  for cc in standalone_ccs[1:]:
    cc_fw_ids = {ref.fw_id for ref in cc.part_of_builtin_frameworks}
    common_ids &= cc_fw_ids
  return [
      ParentFrameworkRef(fw_id=fid, display_name=display_by_id[fid])
      for fid in sorted(common_ids)
  ]


def _validate_cc_parameters(
    cc_id: str,
    selected_parameters: dict[str, Any],
    raw_cc: dict[str, Any],
) -> None:
  """Validates selected parameter keys and allowed string values against spec."""
  if not selected_parameters:
    return
  param_specs = raw_cc.get("parameterSpec", [])
  specs_by_name = {
      ps.get("name"): ps
      for ps in param_specs
      if isinstance(ps, dict) and ps.get("name")
  }
  if not specs_by_name:
    raise ValueError(
        f"CloudControl '{cc_id}' does not accept parameters, but got:"
        f" {list(selected_parameters.keys())}"
    )

  for param_key, param_val in selected_parameters.items():
    if param_key not in specs_by_name:
      raise ValueError(
          f"Invalid parameter '{param_key}' for CloudControl '{cc_id}'."
          f" Allowed parameters: {sorted(specs_by_name.keys())}"
      )
    spec = specs_by_name[param_key]
    allowed_entries = (
        spec.get("validation", {}).get("allowedValues", {}).get("values", [])
    )
    allowed_strings = {
        entry.get("stringValue")
        for entry in allowed_entries
        if isinstance(entry, dict) and "stringValue" in entry
    }
    if allowed_strings:
      candidate_str = (
          param_val.get("stringValue")
          if isinstance(param_val, dict)
          else (param_val if isinstance(param_val, str) else None)
      )
      if candidate_str is not None and candidate_str not in allowed_strings:
        raise ValueError(
            f"Invalid value '{candidate_str}' for parameter '{param_key}' on"
            f" CloudControl '{cc_id}'. Allowed values:"
            f" {sorted(allowed_strings)}"
        )


def _match_percentage(
    satisfied_requirements: list[str], major_requirement_keys: list[str]
) -> float:
  """Returns the percentage of the MAJOR requirements that are satisfied.

  Args:
    satisfied_requirements: The requirements that a Framework satisfies.
    major_requirement_keys: The text of each MAJOR requirement of the intent,
      stripped and in lower case.

  Returns:
    The percentage, rounded to 2 decimals. It is 100.0 when the intent has no
    MAJOR requirement, the same as the overall match score.
  """
  if not major_requirement_keys:
    return 100.0
  satisfied_keys = {r.strip().lower() for r in satisfied_requirements}
  met = sum(1 for key in major_requirement_keys if key in satisfied_keys)
  return round(met / len(major_requirement_keys) * 100.0, 2)


def analyze_output_matches(
    intent: NavigatorIntentSpec,
    match_result: CatalogMatchResult,
    resources: DBResourcesStore,
    include_underlying_ccs: bool = False,
) -> MatchAnalysisReport:
  """Validates matched FWs/CCs, enforces built-in priority, and builds report.

  Args:
    intent: Normalized NavigatorIntentSpec from the user prompt.
    match_result: Candidate frameworks, standalone CCs, and unmatched reqs.
    resources: Loaded DBResourcesStore containing active FWs and CCs.
    include_underlying_ccs: Whether to populate underlying_ccs on matched FWs
      (False by default; set True only when the user explicitly asks for CCs).

  Returns:
    A verified MatchAnalysisReport, with the matched Frameworks sorted from the
    best to the weakest match.

  Raises:
    ValueError: If any fw_id, cc_id, or parameter name/value is invalid.
  """
  req_importance_by_text = {
      r.requirement.strip().lower(): r.importance for r in intent.requirements
  }
  major_requirement_keys = [
      r.requirement.strip().lower()
      for r in intent.requirements
      if r.importance == "MAJOR"
  ]

  verified_fws: list[MatchedFW] = []
  has_builtin_fw = False
  selected_fw_cc_ids: set[str] = set()
  for fw in match_result.selected_frameworks:
    raw_fw = resources.frameworks.get(fw.fw_id)
    if not raw_fw:
      raise ValueError(f"Unknown framework ID in match_result: {fw.fw_id}")

    fw_type = _infer_resource_type(raw_fw, fw.fw_id)
    if fw_type == "BUILT_IN":
      has_builtin_fw = True
    selected_fw_cc_ids |= _framework_cc_ids(raw_fw)

    populated_ccs: list[MatchedCC] | None = None
    if include_underlying_ccs:
      overrides_by_cc = {c.cc_id: c for c in fw.underlying_ccs or []}
      populated_ccs = []
      for ref in raw_fw.get("cloudControlDetails", []):
        cid = ref.get("name", "").split("/")[-1]
        if not cid:
          continue
        raw_cc = resources.cloud_controls.get(cid, {})
        bound_params = {
            p.get("name"): p.get("parameterValue", {})
            for p in ref.get("parameters", [])
            if isinstance(p, dict) and p.get("name")
        }
        override_cc = overrides_by_cc.get(cid)
        if override_cc and override_cc.selected_parameters:
          _validate_cc_parameters(cid, override_cc.selected_parameters, raw_cc)
          bound_params.update(override_cc.selected_parameters)

        populated_ccs.append(
            MatchedCC(
                cc_id=cid,
                cc_type=_infer_resource_type(raw_cc, cid),
                display_name=raw_cc.get(
                    "displayName",
                    override_cc.display_name if override_cc else cid,
                ),
                match_rationale=(
                    override_cc.match_rationale
                    if override_cc and override_cc.match_rationale
                    else raw_cc.get("description", "")
                ),
                matched_rule_types=(
                    _extract_rule_types(raw_cc)
                    or (override_cc.matched_rule_types if override_cc else [])
                ),
                selected_parameters=bound_params,
            )
        )

    verified_fws.append(
        MatchedFW(
            fw_id=fw.fw_id,
            fw_type=fw_type,
            major_revision_id=int(
                raw_fw.get("majorRevisionId", fw.major_revision_id)
            ),
            display_name=raw_fw.get("displayName", fw.display_name),
            match_rationale=(
                fw.match_rationale or raw_fw.get("description", "")
            ),
            satisfied_requirements=list(fw.satisfied_requirements),
            match_percentage=_match_percentage(
                fw.satisfied_requirements, major_requirement_keys
            ),
            underlying_ccs=populated_ccs,
        )
    )

  # Best match first. The sort is stable, so Frameworks with the same
  # percentage keep the order in which they were selected.
  verified_fws.sort(key=lambda fw: fw.match_percentage, reverse=True)

  verified_standalone_ccs: list[MatchedCC] = []
  for cc in match_result.standalone_matched_ccs:
    raw_cc = resources.cloud_controls.get(cc.cc_id)
    if not raw_cc:
      raise ValueError(f"Unknown CloudControl ID in match_result: {cc.cc_id}")
    _validate_cc_parameters(cc.cc_id, cc.selected_parameters, raw_cc)

    # Guardrail: A selected Framework already contains this CloudControl, so it
    # is not an additional one. Matched by ID only; the parameter values that
    # the Framework binds are not compared.
    if cc.cc_id in selected_fw_cc_ids:
      continue

    effective_importance = cc.importance
    if cc.requirement:
      effective_importance = req_importance_by_text.get(
          cc.requirement.strip().lower(), cc.importance
      )

    # Guardrail: If a requirement is minor and not met by the matched built-in
    # framework, ignore recommending extra CCs for it.
    if has_builtin_fw and effective_importance == "MINOR":
      continue

    parent_fws = _resolve_parent_builtin_frameworks(cc.cc_id, raw_cc, resources)
    verified_standalone_ccs.append(
        MatchedCC(
            cc_id=cc.cc_id,
            cc_type=_infer_resource_type(raw_cc, cc.cc_id),
            display_name=raw_cc.get("displayName", cc.display_name),
            requirement=cc.requirement,
            importance=effective_importance,
            match_rationale=(
                cc.match_rationale or raw_cc.get("description", "")
            ),
            part_of_builtin_frameworks=parent_fws,
            matched_rule_types=(
                _extract_rule_types(raw_cc) or list(cc.matched_rule_types)
            ),
            selected_parameters=dict(cc.selected_parameters),
        )
    )

  common_builtin_fws = _compute_common_parent_frameworks(
      verified_standalone_ccs
  )
  # Guardrail: If 1+ additional CCs are all covered by at least one single
  # built-in framework, do NOT suggest clubbing them into a custom framework.
  # Only suggest creating a custom framework for additional CCs when no single
  # built-in framework covers them (e.g. >1 CCs belonging to disjoint built-in
  # frameworks, or an additional CC not in any built-in framework).
  suggest_custom_fw_for_additional_ccs = bool(
      verified_standalone_ccs and not common_builtin_fws
  )

  # Compute unmet MAJOR requirements (ignoring MINOR unmet requirements).
  covered_reqs_lower: set[str] = set()
  for fw in verified_fws:
    for req_str in fw.satisfied_requirements:
      covered_reqs_lower.add(req_str.strip().lower())
  for cc in match_result.standalone_matched_ccs:
    if cc.requirement:
      covered_reqs_lower.add(cc.requirement.strip().lower())

  unmet_major_by_text: dict[str, RequirementItem] = {}
  for req in match_result.unmatched_requirements:
    key = req.requirement.strip().lower()
    effective_imp = req_importance_by_text.get(key, req.importance)
    if effective_imp == "MAJOR" and key:
      req.importance = "MAJOR"
      unmet_major_by_text[key] = req

  for req in intent.requirements:
    key = req.requirement.strip().lower()
    if (
        req.importance == "MAJOR"
        and key
        and key not in covered_reqs_lower
        and key not in unmet_major_by_text
    ):
      unmet_major_by_text[key] = req

  unmet_major_requirements = list(unmet_major_by_text.values())

  total_major_reqs = len(major_requirement_keys)
  match_score_percentage = 100.0
  if total_major_reqs > 0:
    # Count only unmet requirements that are in the intent. The agent can put
    # any text into `unmatched_requirements`, and a requirement that the
    # customer never stated must not lower the score.
    unmet_intent_major_reqs = sum(
        1 for key in major_requirement_keys if key in unmet_major_by_text
    )
    met_major_reqs = total_major_reqs - unmet_intent_major_reqs
    match_score_percentage = (met_major_reqs / total_major_reqs) * 100.0
  match_score_percentage = round(
      max(0.0, min(100.0, match_score_percentage)), 2
  )

  # Guardrail: A built-in Framework is recommended whatever its match percentage
  # is. Custom resources for unmet MAJOR requirements are suggested only when
  # the overall match is less than the threshold.
  suggest_custom_for_unmet_requirements = bool(
      unmet_major_requirements
      and match_score_percentage < CUSTOM_RESOURCES_MATCH_THRESHOLD
  )

  custom_handoff: dict[str, Any] | None = None
  if (
      suggest_custom_for_unmet_requirements
      or suggest_custom_fw_for_additional_ccs
  ):
    custom_handoff = {
        "organization_id": intent.organization_id,
        "location": resources.location,
        "base_frameworks": [f.fw_id for f in verified_fws],
        "additional_existing_ccs_to_bundle": [
            {"cc_id": c.cc_id, "selected_parameters": c.selected_parameters}
            for c in verified_standalone_ccs
        ],
        "unmet_major_requirements_needing_custom_ccs": [
            dataclasses.asdict(r) for r in unmet_major_requirements
        ],
    }

  return MatchAnalysisReport(
      matched_frameworks=verified_fws,
      additional_cloud_controls=verified_standalone_ccs,
      common_builtin_frameworks_for_additional_ccs=common_builtin_fws,
      suggest_custom_framework_for_additional_ccs=(
          suggest_custom_fw_for_additional_ccs
      ),
      unmet_major_requirements=unmet_major_requirements,
      match_score_percentage=match_score_percentage,
      suggest_custom_resources_for_unmet_requirements=(
          suggest_custom_for_unmet_requirements
      ),
      custom_authoring_handoff=custom_handoff,
      location=resources.location,
  )


def write_outputs(
    report: MatchAnalysisReport, output_dir: pathlib.Path
) -> None:
  """Writes the analysis report and, when needed, the author hand-off file.

  `author_handoff.json` is written next to `analysis_report.json` only when the
  report has a hand-off. A file left by an earlier run is removed otherwise, so
  it cannot be mistaken for the hand-off of this run.

  Args:
    report: The verified MatchAnalysisReport.
    output_dir: The directory to write into; it is created if missing.
  """
  output_dir.mkdir(parents=True, exist_ok=True)
  (output_dir / ANALYSIS_REPORT_FILE).write_text(
      json.dumps(report.to_dict(), indent=2)
  )
  handoff_path = output_dir / AUTHOR_HANDOFF_FILE
  if report.custom_authoring_handoff is None:
    handoff_path.unlink(missing_ok=True)
  else:
    handoff_path.write_text(
        json.dumps(report.custom_authoring_handoff, indent=2)
    )


def main() -> None:
  """CLI entry point for validating matches and producing analysis_report.json."""
  parser = argparse.ArgumentParser(
      description="Validates matched DB resources and produces analysis report."
  )
  parser.add_argument("--intent_spec_json", required=True)
  parser.add_argument("--match_result_json", required=True)
  parser.add_argument("--resources_json", required=True)
  parser.add_argument("--output_dir", required=True)
  parser.add_argument(
      "--include_underlying_ccs",
      action="store_true",
      help="Include underlying CloudControls inside matched Frameworks.",
  )
  args = parser.parse_args()

  intent = NavigatorIntentSpec.from_dict(
      json.loads(pathlib.Path(args.intent_spec_json).read_text())
  )
  match_res = CatalogMatchResult.from_dict(
      json.loads(pathlib.Path(args.match_result_json).read_text())
  )
  resources = DBResourcesStore.from_dict(
      json.loads(pathlib.Path(args.resources_json).read_text())
  )
  report = analyze_output_matches(
      intent,
      match_res,
      resources,
      include_underlying_ccs=args.include_underlying_ccs,
  )

  write_outputs(report, pathlib.Path(args.output_dir))


if __name__ == "__main__":
  main()
