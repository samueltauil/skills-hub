"""Cloud Armor OWASP Rule Upgrader CLI.

Translates Cloud Armor security policies from OWASP CRS 3.0/3.3 to OWASP CRS
4.22. Designed for use by Gemini Cloud Assist and Network Security Agents.
"""

from __future__ import annotations

import argparse
import ast
from collections.abc import Mapping, Sequence
import copy
import json
import re
import sys
from typing import Any

# --- Authoritative CRS Mappings & Signatures ---

RULESET_MAPPING: dict[str, str] = {
    # CRS 3.0 Stable
    'sqli-stable': 'sqli-v422-stable',
    'xss-stable': 'xss-v422-stable',
    'lfi-stable': 'lfi-v422-stable',
    'rfi-stable': 'rfi-v422-stable',
    'rce-stable': 'rce-v422-stable',
    'methodenforcement-stable': 'methodenforcement-v422-stable',
    'scannerdetection-stable': 'scannerdetection-v422-stable',
    'protocolattack-stable': 'protocolattack-v422-stable',
    'php-stable': 'php-v422-stable',
    'sessionfixation-stable': 'sessionfixation-v422-stable',
    # CRS 3.0 Canary
    'sqli-canary': 'sqli-v422-canary',
    'xss-canary': 'xss-v422-canary',
    'lfi-canary': 'lfi-v422-canary',
    'rfi-canary': 'rfi-v422-canary',
    'rce-canary': 'rce-v422-canary',
    'methodenforcement-canary': 'methodenforcement-v422-canary',
    'scannerdetection-canary': 'scannerdetection-v422-canary',
    'protocolattack-canary': 'protocolattack-v422-canary',
    'php-canary': 'php-v422-canary',
    'sessionfixation-canary': 'sessionfixation-v422-canary',
    # CRS 3.3 Stable
    'sqli-v33-stable': 'sqli-v422-stable',
    'xss-v33-stable': 'xss-v422-stable',
    'lfi-v33-stable': 'lfi-v422-stable',
    'rfi-v33-stable': 'rfi-v422-stable',
    'rce-v33-stable': 'rce-v422-stable',
    'methodenforcement-v33-stable': 'methodenforcement-v422-stable',
    'scannerdetection-v33-stable': 'scannerdetection-v422-stable',
    'protocolattack-v33-stable': 'protocolattack-v422-stable',
    'php-v33-stable': 'php-v422-stable',
    'sessionfixation-v33-stable': 'sessionfixation-v422-stable',
    'java-v33-stable': 'java-v422-stable',
    'nodejs-v33-stable': 'generic-v422-stable',
    # CRS 3.3 Canary
    'sqli-v33-canary': 'sqli-v422-canary',
    'xss-v33-canary': 'xss-v422-canary',
    'lfi-v33-canary': 'lfi-v422-canary',
    'rfi-v33-canary': 'rfi-v422-canary',
    'rce-v33-canary': 'rce-v422-canary',
    'methodenforcement-v33-canary': 'methodenforcement-v422-canary',
    'scannerdetection-v33-canary': 'scannerdetection-v422-canary',
    'protocolattack-v33-canary': 'protocolattack-v422-canary',
    'php-v33-canary': 'php-v422-canary',
    'sessionfixation-v33-canary': 'sessionfixation-v422-canary',
    'java-v33-canary': 'java-v422-canary',
    'nodejs-v33-canary': 'generic-v422-canary',
    # Standalone / Special Rulesets
    'cve-canary': 'cve-canary',
}

_SIGNATURE_COUNTS_30: dict[tuple[str, int], tuple[int, int]] = {
    ('sqli', 4): (38, 60),
    ('xss', 4): (25, 33),
    ('lfi', 4): (4, 5),
    ('rce', 4): (11, 44),
    ('rfi', 4): (4, 5),
    ('php', 4): (13, 20),
    ('protocolattack', 4): (9, 17),
    ('sessionfixation', 4): (3, 3),
    ('methodenforcement', 4): (1, 1),
    ('scannerdetection', 4): (5, 1),
}

_SIGNATURE_COUNTS_33: dict[tuple[str, int], tuple[int, int]] = {
    ('sqli', 4): (49, 60),
    ('xss', 4): (30, 33),
    ('lfi', 4): (4, 5),
    ('rce', 4): (15, 44),
    ('rfi', 4): (4, 5),
    ('php', 4): (16, 20),
    ('protocolattack', 4): (10, 17),
    ('sessionfixation', 4): (3, 3),
    ('methodenforcement', 4): (1, 1),
    ('scannerdetection', 4): (5, 1),
    ('java', 4): (9, 14),
    ('generic', 4): (1, 10),
    ('nodejs', 4): (1, 10),
}

_VALID_CRS422_SIGNATURE_NUMBERS: frozenset[str] = frozenset({
    '911100',
    '913100',
    '921110',
    '921120',
    '921130',
    '921140',
    '921150',
    '921151',
    '921160',
    '921170',
    '921190',
    '921200',
    '921210',
    '921220',
    '921230',
    '921240',
    '921250',
    '921421',
    '921422',
    '930100',
    '930110',
    '930120',
    '930121',
    '930130',
    '931100',
    '931110',
    '931120',
    '931130',
    '931131',
    '932120',
    '932125',
    '932130',
    '932131',
    '932140',
    '932160',
    '932161',
    '932170',
    '932171',
    '932175',
    '932180',
    '932190',
    '932200',
    '932205',
    '932206',
    '932207',
    '932210',
    '932220',
    '932230',
    '932231',
    '932232',
    '932235',
    '932236',
    '932237',
    '932238',
    '932239',
    '932240',
    '932250',
    '932260',
    '932270',
    '932271',
    '932280',
    '932281',
    '932300',
    '932301',
    '932310',
    '932311',
    '932320',
    '932321',
    '932330',
    '932331',
    '932370',
    '932371',
    '932380',
    '933100',
    '933110',
    '933111',
    '933120',
    '933130',
    '933131',
    '933135',
    '933140',
    '933150',
    '933151',
    '933152',
    '933153',
    '933160',
    '933161',
    '933170',
    '933180',
    '933190',
    '933200',
    '933210',
    '933211',
    '934100',
    '934101',
    '934110',
    '934120',
    '934130',
    '934140',
    '934150',
    '934160',
    '934170',
    '934180',
    '941100',
    '941101',
    '941110',
    '941120',
    '941130',
    '941140',
    '941150',
    '941160',
    '941170',
    '941180',
    '941181',
    '941190',
    '941200',
    '941210',
    '941220',
    '941230',
    '941240',
    '941250',
    '941260',
    '941270',
    '941280',
    '941290',
    '941300',
    '941310',
    '941320',
    '941330',
    '941340',
    '941350',
    '941360',
    '941370',
    '941380',
    '941390',
    '941400',
    '942100',
    '942101',
    '942120',
    '942130',
    '942131',
    '942140',
    '942150',
    '942151',
    '942152',
    '942160',
    '942170',
    '942180',
    '942190',
    '942200',
    '942210',
    '942220',
    '942230',
    '942240',
    '942250',
    '942251',
    '942260',
    '942270',
    '942280',
    '942290',
    '942300',
    '942310',
    '942320',
    '942321',
    '942330',
    '942340',
    '942350',
    '942360',
    '942361',
    '942362',
    '942370',
    '942380',
    '942390',
    '942400',
    '942410',
    '942420',
    '942421',
    '942430',
    '942431',
    '942432',
    '942440',
    '942450',
    '942460',
    '942470',
    '942480',
    '942490',
    '942500',
    '942510',
    '942511',
    '942520',
    '942521',
    '942522',
    '942530',
    '942540',
    '942550',
    '942560',
    '943100',
    '943110',
    '943120',
    '944100',
    '944110',
    '944120',
    '944130',
    '944140',
    '944150',
    '944151',
    '944152',
    '944200',
    '944210',
    '944240',
    '944250',
    '944260',
    '944300',
})

_DEPRECATED_SIGNATURE_NUMBERS: frozenset[str] = frozenset({
    '981172',
    '981173',
    '980130',
    '949110',
    '942110',
    '932100',
    '932105',
    '932106',
    '932110',
    '932115',
    '932150',
    '913101',
    '913102',
    '913110',
    '913120',
})

_RE_DANGLING_ID_PATTERN = re.compile(
    r'\bid(' + '|'.join(sorted(_DEPRECATED_SIGNATURE_NUMBERS)) + r')\b',
    re.IGNORECASE,
)

_VALID_CVE_SIGNATURE_NUMBERS: frozenset[str] = frozenset({
    '044228',
    '144228',
    '244228',
    '344228',
})

_RE_WAF_EXPR_PATTERN = re.compile(
    r'(evaluatePreconfiguredWaf|evaluatePreconfiguredExpr)\s*\(\s*'
    r'([\'"])([^\'"]+)\2\s*(?:,\s*(\[[\s\S]*?\]|\{(?:[^{}]|\{[^{}]*\})*\}))?'
    r'\s*\)',
    re.IGNORECASE,
)

_RE_CRS_SIGNATURE_FULL = re.compile(r'owasp-crs-v\d{6}-(id\d+-[a-z0-9]+)')
_RE_SIGNATURE_NUMBER = re.compile(r'\bid(\d+)\b', re.IGNORECASE)
_RE_IN_IP_RANGE = re.compile(r'\binIPRange\b')

# Backward-compatibility aliases
SIGNATURE_COUNTS_30 = _SIGNATURE_COUNTS_30
SIGNATURE_COUNTS_33 = _SIGNATURE_COUNTS_33
VALID_CRS422_SIGNATURE_NUMBERS = _VALID_CRS422_SIGNATURE_NUMBERS
VALID_CVE_SIGNATURE_NUMBERS = _VALID_CVE_SIGNATURE_NUMBERS
DEPRECATED_SIGNATURE_NUMBERS = _DEPRECATED_SIGNATURE_NUMBERS
DANGLING_ID_PATTERN = _RE_DANGLING_ID_PATTERN
WAF_EXPR_PATTERN = _RE_WAF_EXPR_PATTERN


# --- Transformation Functions ---


def is_cve_signature(signature_id: str) -> bool:
  """Checks whether a signature ID belongs to a standalone CVE rule.

  Args:
    signature_id: The signature identifier string.

  Returns:
    True if the signature belongs to a standalone CVE rule, False otherwise.
  """
  if not signature_id:
    return False
  sig_clean = signature_id.strip().lower()
  if '-cve' in sig_clean or 'google-mrs-' in sig_clean:
    return True
  match = _RE_SIGNATURE_NUMBER.search(sig_clean)
  if match and match.group(1) in _VALID_CVE_SIGNATURE_NUMBERS:
    return True
  return False


def is_422_ruleset(name: str) -> bool:
  """Checks whether a ruleset name belongs to OWASP CRS 4.22.

  Args:
    name: The ruleset name string.

  Returns:
    True if the ruleset is an OWASP CRS 4.22 ruleset, False otherwise.
  """
  if not name:
    return False
  return 'v422' in name.lower() or name in RULESET_MAPPING.values()


def is_known_ruleset(name: str) -> bool:
  """Checks whether a ruleset name is recognized in CRS 3.0, 3.3, or 4.22.

  Args:
    name: The ruleset name string.

  Returns:
    True if the ruleset is known, False otherwise.
  """
  if not name:
    return False
  return name in RULESET_MAPPING or is_422_ruleset(name)


def translate_ruleset_name(name: str) -> str:
  """Translates a legacy CRS 3.0 or 3.3 ruleset name to CRS 4.22.

  Args:
    name: The legacy ruleset name.

  Returns:
    The corresponding CRS 4.22 ruleset name, or the original name if unmapped.
  """
  if not name:
    return name
  return RULESET_MAPPING.get(name, name)


def _replace_crs_sig(match: re.Match[str]) -> str:
  """Regex substitution callback for legacy CRS signature IDs."""
  suffix = match.group(1)
  if suffix.endswith('-cve'):
    return match.group(0)
  if suffix.endswith('-nodejs'):
    suffix = suffix[:-7] + '-generic'
  return f'owasp-crs-v042200-{suffix}'


def translate_signature_id(signature_id: str) -> str:
  """Translates a legacy signature ID to CRS 4.22 format (v042200).

  Args:
    signature_id: The signature identifier string.

  Returns:
    The remapped signature ID with 'owasp-crs-v042200-'.
  """
  if not signature_id:
    return signature_id

  return _RE_CRS_SIGNATURE_FULL.sub(_replace_crs_sig, signature_id)


def check_dangling_signature_id(signature_id: str) -> bool:
  """Checks if a signature ID is deprecated or not in the CRS 4.22 catalog.

  Args:
    signature_id: The signature identifier string.

  Returns:
    True if the signature is dangling/retired in CRS 4.22, False otherwise.
  """
  if not signature_id:
    return False
  sig_clean = signature_id.strip()
  if bool(_RE_DANGLING_ID_PATTERN.search(sig_clean)):
    return True
  if is_cve_signature(sig_clean):
    return False
  match = _RE_SIGNATURE_NUMBER.search(sig_clean)
  if match:
    num = match.group(1)
    if num not in _VALID_CRS422_SIGNATURE_NUMBERS:
      return True
  return False


def filter_dangling_signature_ids(ids: Sequence[str]) -> list[str]:
  """Filters out dangling or retired signature IDs from a sequence of IDs.

  Args:
    ids: A sequence of signature identifier strings.

  Returns:
    A list of valid CRS 4.22 signature IDs.
  """
  if not ids:
    return []
  return [i for i in ids if not check_dangling_signature_id(i)]


def get_signature_counts(
    old_ruleset: str,
    sensitivity: int = 4,
) -> tuple[int, int] | None:
  """Retrieves signature counts (old vs new) for a ruleset.

  Args:
    old_ruleset: The legacy ruleset identifier.
    sensitivity: Sensitivity level (default: 4).

  Returns:
    A tuple of (old_count, new_count), or None if not found.
  """
  if not old_ruleset:
    return None
  if 'v33' in old_ruleset:
    cat = old_ruleset.split('-')[0].replace('v33', '').strip()
    return _SIGNATURE_COUNTS_33.get((cat, sensitivity))
  cat = old_ruleset.split('-')[0].strip()
  return _SIGNATURE_COUNTS_30.get(
      (cat, sensitivity)
  ) or _SIGNATURE_COUNTS_33.get((cat, sensitivity))


def _clean_opt_out_structure(obj: Any) -> tuple[Any, bool, bool]:
  """Recursively cleans opt-out/in structures.

  Remaps IDs and drops retired ones.

  Args:
    obj: The data structure (list, dict, or str) to clean.

  Returns:
    A tuple of (cleaned_obj, sig_remapped, dangling_detected).
  """
  sig_remapped = False
  dangling_detected = False

  if isinstance(obj, list):
    valid_list = []
    for item in obj:
      cleaned_item, remapped, dangling = _clean_opt_out_structure(item)
      if remapped:
        sig_remapped = True
      if dangling:
        dangling_detected = True
      if cleaned_item is not None:
        valid_list.append(cleaned_item)
    return valid_list, sig_remapped, dangling_detected

  if isinstance(obj, dict):
    cleaned_dict = {}
    for k, v in obj.items():
      if k in ('opt_out_rule_ids', 'opt_in_rule_ids') and isinstance(v, list):
        valid_ids = []
        for item in v:
          if check_dangling_signature_id(item):
            dangling_detected = True
          else:
            trans = translate_signature_id(item)
            if trans != item:
              sig_remapped = True
            valid_ids.append(trans)
        cleaned_dict[k] = valid_ids
      else:
        cleaned_v, remapped, dangling = _clean_opt_out_structure(v)
        if remapped:
          sig_remapped = True
        if dangling:
          dangling_detected = True
        if cleaned_v is not None:
          cleaned_dict[k] = cleaned_v
    return cleaned_dict, sig_remapped, dangling_detected

  if isinstance(obj, str):
    if check_dangling_signature_id(obj):
      return None, sig_remapped, True
    trans = translate_signature_id(obj)
    if trans != obj:
      sig_remapped = True
    return trans, sig_remapped, dangling_detected

  return obj, sig_remapped, dangling_detected


def _clean_extra_arg(
    extra_arg: str,
    func_name: str,
) -> tuple[str, bool, bool]:
  """Cleans the optional configuration argument to a WAF evaluation function.

  Args:
    extra_arg: Raw argument string from the expression.
    func_name: The enclosing function name (e.g. evaluatePreconfiguredExpr).

  Returns:
    A tuple of (cleaned_arg_str, sig_remapped, dangling_detected).
  """
  if not extra_arg:
    return extra_arg, False, False

  sig_remapped = False
  dangling_detected = check_dangling_signature_id(extra_arg)

  try:
    parsed_val = ast.literal_eval(extra_arg)
  except (ValueError, SyntaxError, MemoryError, RecursionError):
    # If extra_arg is not a valid Python literal expression, treat it as a
    # raw string.
    pass
  else:
    if isinstance(parsed_val, list):
      cleaned_list, remapped, dangling = _clean_opt_out_structure(parsed_val)
      cleaned_dict = {'opt_out_rule_ids': cleaned_list}
      return repr(cleaned_dict), remapped, (dangling_detected or dangling)
    if isinstance(parsed_val, dict):
      cleaned_dict, remapped, dangling = _clean_opt_out_structure(parsed_val)
      return repr(cleaned_dict), remapped, (dangling_detected or dangling)

  translated_arg = translate_signature_id(extra_arg)
  if translated_arg != extra_arg:
    sig_remapped = True

  if (
      func_name.lower() == 'evaluatepreconfiguredexpr'
      and translated_arg.startswith('[')
  ):
    translated_arg = f"{{'opt_out_rule_ids': {translated_arg}}}"

  return translated_arg, sig_remapped, dangling_detected


def transform_expression(expression: str) -> dict[str, Any]:
  """Transforms a Cloud Armor CEL rule expression to CRS 4.22.

  Args:
    expression: The CEL expression string.

  Returns:
    A dictionary containing the transformed expression and metadata:
      - 'new_expression': The updated CEL expression.
      - 'old_ruleset': The legacy ruleset identifier found.
      - 'new_ruleset': The target CRS 4.22 ruleset identifier.
      - 'old_rulesets': List of legacy ruleset identifiers found.
      - 'new_rulesets': List of target CRS 4.22 ruleset identifiers.
      - 'sig_id_remapped': Whether any signature IDs were remapped.
      - 'dangling_id_detected': Whether any deprecated IDs were dropped.
      - 'is_already_422': Whether the expression was already using CRS 4.22.
  """
  if expression:
    expression = expression.strip()

  sig_id_remapped = False
  dangling_id_detected = False
  old_rulesets: list[str] = []
  new_rulesets: list[str] = []
  matched_422_flags: list[bool] = []

  def _replace_ruleset(match: re.Match[str]) -> str:
    nonlocal sig_id_remapped, dangling_id_detected
    func_name = match.group(1)
    quote = match.group(2)
    old_rs = match.group(3)
    extra_arg = match.group(4)

    old_rulesets.append(old_rs)
    if not is_known_ruleset(old_rs):
      target_rs = old_rs
    else:
      target_rs = translate_ruleset_name(old_rs)
    new_rulesets.append(target_rs)

    is_match_422 = (
        is_422_ruleset(old_rs) or old_rs == target_rs
    ) and is_422_ruleset(target_rs)
    matched_422_flags.append(is_match_422)

    new_func_name = 'evaluatePreconfiguredWaf'

    if extra_arg:
      cleaned_arg, remapped, dangling = _clean_extra_arg(extra_arg, func_name)
      if remapped:
        sig_id_remapped = True
      if dangling:
        dangling_id_detected = True

      if cleaned_arg and cleaned_arg not in ("{'opt_out_rule_ids': []}", '{}'):
        return f'{new_func_name}({quote}{target_rs}{quote}, {cleaned_arg})'

    return f'{new_func_name}({quote}{target_rs}{quote})'

  new_expr = _RE_WAF_EXPR_PATTERN.sub(_replace_ruleset, expression)

  if 'owasp-crs-v030' in new_expr:
    new_expr_sig = translate_signature_id(new_expr)
    if new_expr_sig != new_expr:
      sig_id_remapped = True
      new_expr = new_expr_sig

  if check_dangling_signature_id(new_expr):
    dangling_id_detected = True

  if 'inIPRange' in new_expr:
    new_expr = _RE_IN_IP_RANGE.sub('inIpRange', new_expr)

  old_ruleset = ', '.join(old_rulesets) if old_rulesets else 'unknown'
  new_ruleset = ', '.join(new_rulesets) if new_rulesets else 'unknown'
  is_already_422 = (
      bool(matched_422_flags)
      and all(matched_422_flags)
      and not sig_id_remapped
      and not dangling_id_detected
  )

  return {
      'new_expression': new_expr,
      'old_ruleset': old_ruleset,
      'new_ruleset': new_ruleset,
      'old_rulesets': old_rulesets,
      'new_rulesets': new_rulesets,
      'sig_id_remapped': sig_id_remapped,
      'dangling_id_detected': dangling_id_detected,
      'is_already_422': is_already_422,
  }


def transform_preconfigured_waf_config(
    waf_config: Mapping[str, Any] | None,
) -> tuple[dict[str, Any] | None, bool, bool]:
  """Transforms a preconfiguredWafConfig structure to CRS 4.22.

  Args:
    waf_config: The preconfiguredWafConfig dictionary, or None.

  Returns:
    A tuple of (updated_config, remapped, dangling) where:
      - updated_config: The updated config dictionary, or None if input
        was None.
      - remapped: True if any signature IDs were remapped.
      - dangling: True if any deprecated signature IDs were dropped.
  """
  if not waf_config or not isinstance(waf_config, (dict, Mapping)):
    return None if waf_config is None else {}, False, False

  updated_config = copy.deepcopy(dict(waf_config))
  exclusions = updated_config.get('exclusions', [])
  remapped = False
  dangling = False
  new_exclusions = []

  for exclusion in exclusions:
    if 'targetRuleSet' in exclusion:
      old_rs = exclusion['targetRuleSet']
      exclusion['targetRuleSet'] = translate_ruleset_name(old_rs)

    if 'targetRuleIds' in exclusion and isinstance(
        exclusion['targetRuleIds'], list
    ):
      had_target_rule_ids = bool(exclusion['targetRuleIds'])
      valid_ids = filter_dangling_signature_ids(exclusion['targetRuleIds'])
      if len(valid_ids) < len(exclusion['targetRuleIds']):
        dangling = True

      translated_ids = []
      for r_id in valid_ids:
        translated = translate_signature_id(r_id)
        if translated != r_id:
          remapped = True
        translated_ids.append(translated)
      if had_target_rule_ids and not translated_ids:
        continue
      exclusion['targetRuleIds'] = translated_ids

    new_exclusions.append(exclusion)

  updated_config['exclusions'] = new_exclusions
  return updated_config, remapped, dangling


def _is_rule_already_422(
    original_expr: str,
    tx_res: Mapping[str, Any],
    waf_cfg: Mapping[str, Any] | None,
    updated_waf_cfg: Mapping[str, Any] | None,
    waf_remapped: bool,
    waf_dangling: bool,
) -> bool:
  """Checks whether a WAF rule and its exclusions are already on CRS 4.22."""
  if not tx_res.get('is_already_422'):
    return False
  if tx_res.get('new_expression') != original_expr.strip():
    return False
  if waf_remapped or waf_dangling:
    return False
  if waf_cfg and updated_waf_cfg != waf_cfg:
    return False
  return True


def upgrade_policy(
    policy: Mapping[str, Any],
    mode: str = 'in-place',
    preview_priority_offset: int = 5,
) -> tuple[dict[str, Any], dict[str, Any]]:
  """Upgrades a Cloud Armor policy dictionary from CRS 3.0/3.3 to CRS 4.22.

  Args:
    policy: The security policy dictionary containing 'rules'.
    mode: Upgrade mode, either 'in-place' or 'preview'.
    preview_priority_offset: Priority offset for preview rules (default: 5).

  Returns:
    A tuple of (upgraded_policy_dict, audit_report_dict).

  Raises:
    ValueError: If preview mode exceeds the 200-rule limit or if preview
      priority slots cannot be allocated.
  """
  rules = copy.deepcopy(list(policy.get('rules', [])))
  rules.sort(key=lambda r: r.get('priority', 2147483647))

  total_rules = len(rules)
  upgraded_rules = []
  rule_summaries = []
  method_enforcement_warned = False
  deprecated_signatures_found = []

  # Quota check for preview mode
  in_scope_rules_count = 0
  for r in rules:
    expr = r.get('match', {}).get('expr', {}).get('expression', '')
    if _RE_WAF_EXPR_PATTERN.search(expr):
      tx_check = transform_expression(expr)
      waf_cfg_check = r.get('preconfiguredWafConfig')
      upd_waf_check, w_remap, w_dang = transform_preconfigured_waf_config(
          waf_cfg_check
      )
      if not _is_rule_already_422(
          expr, tx_check, waf_cfg_check, upd_waf_check, w_remap, w_dang
      ):
        in_scope_rules_count += 1

  if mode == 'preview':
    projected_total = total_rules + in_scope_rules_count
    if projected_total > 200:
      raise ValueError(
          f'Cloud Armor Quota Exceeded: Generating preview rules would result'
          f" in {projected_total} rules, exceeding Google Cloud Armor's"
          ' maximum limit of 200 rules per security policy. The upgrade'
          ' cannot proceed in preview mode. Consider an in-place upgrade'
          ' or consolidating rules.'
      )

  occupied_priorities: set[int] = {
      r.get('priority') for r in rules if 'priority' in r
  }

  for index, r in enumerate(rules):
    prio = r.get('priority')
    previous_priority = (
        rules[index - 1].get('priority', -1) if index > 0 else -1
    )
    desc = r.get('description', '')
    action = r.get('action', 'deny(403)')
    expr_obj = r.get('match', {}).get('expr', {})
    original_expr = (
        expr_obj.get('expression', '') if isinstance(expr_obj, dict) else ''
    )
    waf_cfg = r.get('preconfiguredWafConfig')

    is_waf = bool(_RE_WAF_EXPR_PATTERN.search(original_expr))

    if not is_waf:
      # Pass-through rule unchanged
      upgraded_rules.append(r)
      rule_summaries.append({
          'priority': prio,
          'type': 'pass-through',
          'risk_level': 'NONE',
          'impact_category': 'Pass-Through',
          'reason': 'Non-WAF rule (carried over unchanged)',
      })
      continue

    # Transform expression
    tx_res = transform_expression(original_expr)
    upgraded_expr = tx_res['new_expression']
    old_rs = tx_res['old_ruleset']
    new_rs = tx_res['new_ruleset']

    # Transform preconfiguredWafConfig if present
    updated_waf_cfg, waf_remapped, waf_dangling = (
        transform_preconfigured_waf_config(waf_cfg)
    )

    if _is_rule_already_422(
        original_expr,
        tx_res,
        waf_cfg,
        updated_waf_cfg,
        waf_remapped,
        waf_dangling,
    ):
      upgraded_rules.append(r)
      rule_summaries.append({
          'priority': prio,
          'type': 'pass-through',
          'risk_level': 'NONE',
          'impact_category': 'Pass-Through',
          'reason': 'Already using CRS 4.22 (carried over unchanged)',
      })
      continue

    dangling = tx_res['dangling_id_detected'] or waf_dangling
    if dangling:
      deprecated_signatures_found.append(prio)

    is_method_enf = any(
        'methodenforcement' in rs.lower()
        for rs in (tx_res['old_rulesets'] + tx_res['new_rulesets'])
    )
    if is_method_enf:
      method_enforcement_warned = True

    sig_counts = None
    for candidate_rs in tx_res['old_rulesets']:
      counts = get_signature_counts(candidate_rs, sensitivity=4)
      if counts and (
          sig_counts is None
          or (counts[1] - counts[0]) > (sig_counts[1] - sig_counts[0])
      ):
        sig_counts = counts

    # Operational Risk Classification (High / Medium / Low)
    if is_method_enf:
      risk_level = 'HIGH'
      impact_category = 'Breaking Change'
      risk_reasons = [
          (
              'Method Enforcement in CRS 4.22 permits only GET, HEAD, POST,'
              ' OPTIONS. Requests with PUT, PATCH, DELETE are blocked.'
          ),
      ]
    elif dangling or (sig_counts and sig_counts[1] > sig_counts[0] + 5):
      risk_level = 'MEDIUM'
      impact_category = 'Attention Required'
      risk_reasons = []
      if dangling:
        risk_reasons.append(
            'Legacy signature ID was retired in CRS 4.22 and omitted from'
            ' opt-outs.'
        )
      if sig_counts and sig_counts[1] > sig_counts[0] + 5:
        risk_reasons.append(
            f'Coverage expansion: signatures increased from {sig_counts[0]}'
            f' to {sig_counts[1]}.'
        )
    else:
      risk_level = 'LOW'
      impact_category = 'Clean Upgrade'
      risk_reasons = [
          'Direct ruleset translation with no expected behavioral divergence.',
      ]

    rule_summary = {
        'priority': prio,
        'old_ruleset': old_rs,
        'new_ruleset': new_rs,
        'original_expression': original_expr,
        'upgraded_expression': upgraded_expr,
        'signature_counts': sig_counts,
        'dangling_signatures_dropped': dangling,
        'method_enforcement_risk': is_method_enf,
        'risk_level': risk_level,
        'impact_category': impact_category,
        'risk_reasons': risk_reasons,
    }
    rule_summaries.append(rule_summary)

    if mode == 'in-place':
      upgraded_r = copy.deepcopy(r)
      upgraded_r['match']['expr']['expression'] = upgraded_expr
      if updated_waf_cfg is not None:
        if updated_waf_cfg.get('exclusions'):
          upgraded_r['preconfiguredWafConfig'] = updated_waf_cfg
        else:
          upgraded_r.pop('preconfiguredWafConfig', None)
      upgraded_rules.append(upgraded_r)
    elif mode == 'preview':
      # Keep original enforcing rule
      upgraded_rules.append(r)

      # Find preview priority lower than prio (higher evaluation priority),
      # strictly bounded above previous_priority so the preview rule never
      # crosses an intervening allow/deny rule.
      candidate_prio = prio - preview_priority_offset
      if (
          candidate_prio <= previous_priority
          or candidate_prio in occupied_priorities
      ):
        # Find available priority downwards within (previous_priority, prio)
        found = False
        for candidate in range(prio - 1, previous_priority, -1):
          if candidate not in occupied_priorities:
            candidate_prio = candidate
            found = True
            break
        if not found:
          if previous_priority >= 0:
            raise ValueError(
                f'Cannot allocate preview priority for rule {prio}: no free'
                f' slots below {prio} and above preceding rule at priority'
                f' {previous_priority}. Please readjust your rule priorities to'
                ' leave at least one open priority number between'
                f' {previous_priority} and {prio}, or perform an in-place'
                ' upgrade.'
            )
          raise ValueError(
              f'Cannot allocate preview priority for rule {prio}: no free'
              f' slots below {prio}. Please readjust this rule to priority 1'
              ' or higher to leave room for a preview rule, or perform an'
              ' in-place upgrade.'
          )

      occupied_priorities.add(candidate_prio)
      rule_summary['preview_priority'] = candidate_prio

      preview_r = copy.deepcopy(r)
      preview_r['priority'] = candidate_prio
      preview_r['preview'] = True
      preview_r['action'] = action
      preview_r['description'] = (
          f'PREVIEW: Upgraded CRS 4.22 Rule (Target Priority {prio}) - {desc}'
      ).strip(' -')
      preview_r['match']['expr']['expression'] = upgraded_expr
      if updated_waf_cfg is not None:
        if updated_waf_cfg.get('exclusions'):
          preview_r['preconfiguredWafConfig'] = updated_waf_cfg
        else:
          preview_r.pop('preconfiguredWafConfig', None)
      upgraded_rules.append(preview_r)

  # Re-sort rules by priority ascending
  upgraded_rules.sort(key=lambda x: x.get('priority', 2147483647))

  upgraded_policy = copy.deepcopy(dict(policy))
  upgraded_policy['rules'] = upgraded_rules

  report = {
      'policy_name': policy.get('name', 'unnamed_policy'),
      'mode': mode,
      'total_rules_original': total_rules,
      'total_rules_upgraded': len(upgraded_rules),
      'in_scope_waf_rules': in_scope_rules_count,
      'method_enforcement_warning': method_enforcement_warned,
      'rules_with_deprecated_signatures': deprecated_signatures_found,
      'rule_summaries': rule_summaries,
  }

  return upgraded_policy, report


def generate_gcloud_commands(
    policy: Mapping[str, Any],
    report: Mapping[str, Any],
) -> list[str]:
  """Generates sequential gcloud CLI commands to apply the upgrade.

  Args:
    policy: The upgraded security policy dictionary.
    report: The audit report dictionary returned by upgrade_policy.

  Returns:
    A list of gcloud CLI command strings.
  """
  commands = []
  pol_name = report['policy_name']
  mode = report['mode']

  header_mode = mode.upper()
  commands.append(
      f'# === Cloud Armor Upgrade Commands ({header_mode} MODE) ==='
  )
  commands.append(f'# Policy: {pol_name}\n')

  if report.get('method_enforcement_warning'):
    commands.append('# [CRITICAL WARNING] Method Enforcement rule detected.')
    commands.append(
        '# CRS 4.22 blocks PUT, PATCH, DELETE methods. Ensure API endpoints'
        ' are exempted before cutover.\n'
    )

  if mode == 'in-place':
    for r in report['rule_summaries']:
      if r.get('type') == 'pass-through':
        continue
      prio = r['priority']
      expr = r['upgraded_expression']
      commands.append(
          f'gcloud compute security-policies rules update {prio} \\\n'
          f'  --security-policy="{pol_name}" \\\n'
          f'  --expression="{expr}"'
      )
  elif mode == 'preview':
    for r in policy.get('rules', []):
      desc = r.get('description', '')
      if r.get('preview') and desc.startswith(
          'PREVIEW: Upgraded CRS 4.22 Rule'
      ):
        prio = r['priority']
        action = r.get('action', 'deny(403)')
        expr = r.get('match', {}).get('expr', {}).get('expression')
        if not expr:
          continue
        commands.append(
            f'gcloud compute security-policies rules create {prio} \\\n'
            f'  --security-policy="{pol_name}" \\\n'
            f'  --expression="{expr}" \\\n'
            f'  --action="{action}" \\\n'
            '  --preview \\\n'
            f'  --description="{desc}"'
        )

  return commands


# --- Main CLI ---


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
  """Parses command-line arguments."""
  parser = argparse.ArgumentParser(
      description=(
          'Cloud Armor OWASP Rule Upgrader CLI. Translates Cloud Armor security'
          ' policies from OWASP CRS 3.0/3.3 to OWASP CRS 4.22.'
      )
  )
  parser.add_argument(
      'positional_input_file',
      nargs='?',
      default=None,
      metavar='input_file',
      help="Path to policy JSON file, or '-' for stdin.",
  )
  parser.add_argument(
      '--input_file',
      default='-',
      help="Path to policy JSON file, or '-' for stdin.",
  )
  parser.add_argument(
      '--mode',
      choices=['in-place', 'preview'],
      default='in-place',
      help='Upgrade mode.',
  )
  parser.add_argument(
      '--format',
      choices=['json', 'gcloud', 'report'],
      default='json',
      help='Output format.',
  )
  parser.add_argument(
      '--preview_offset',
      type=int,
      default=5,
      help='Priority offset for preview rules.',
  )
  return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
  """Main entry point for the Cloud Armor OWASP Rule Upgrader CLI."""
  args = parse_args(argv)
  input_file = args.positional_input_file or args.input_file
  mode = args.mode
  out_format = args.format
  preview_offset = args.preview_offset

  if input_file == '-':
    content = sys.stdin.read()
  else:
    with open(input_file, 'r', encoding='utf-8') as f:
      content = f.read()

  if not content.strip():
    sys.stderr.write('Error: Empty policy input.\n')
    sys.exit(1)

  try:
    policy = json.loads(content)
  except json.JSONDecodeError as err:
    sys.stderr.write(f'Error: Invalid JSON policy ({err})\n')
    sys.exit(1)

  if isinstance(policy, list):
    if len(policy) == 1 and isinstance(policy[0], dict):
      policy = policy[0]
    else:
      sys.stderr.write(
          'Error: Expected a single security policy JSON object or a list with'
          f' one policy, but received a list of {len(policy)} items.\n'
      )
      sys.exit(1)

  try:
    upgraded_pol, report = upgrade_policy(
        policy,
        mode=mode,
        preview_priority_offset=preview_offset,
    )
  except ValueError as err:
    sys.stderr.write(f'Error: {err}\n')
    sys.exit(1)

  if out_format == 'json':
    print(json.dumps(upgraded_pol, indent=2))
  elif out_format == 'gcloud':
    cmds = generate_gcloud_commands(upgraded_pol, report)
    print('\n'.join(cmds))
  elif out_format == 'report':
    print(f"Policy: {report['policy_name']} (Mode: {report['mode']})")
    print(
        f"Total Rules: {report['total_rules_original']} ->"
        f" {report['total_rules_upgraded']}"
    )
    print(f"WAF Rules Upgraded: {report['in_scope_waf_rules']}")
    if report['method_enforcement_warning']:
      print(
          'ALERT [High Risk / Breaking Change]: Method Enforcement rule'
          ' detected! Blocks PUT/PATCH/DELETE in CRS 4.22.'
      )
    if report['rules_with_deprecated_signatures']:
      print(
          'Attention Required [Medium Risk]: Deprecated Signatures Dropped in'
          f" Rules: {report['rules_with_deprecated_signatures']}"
      )
    print('\nRule Breakdown:')
    for s in report['rule_summaries']:
      if s.get('type') == 'pass-through':
        print(f"  Priority {s['priority']} [No Action]: Pass-through (non-WAF)")
      else:
        cnt = (
            f" ({s['signature_counts'][0]} -> {s['signature_counts'][1]} sigs)"
            if s.get('signature_counts')
            else ''
        )
        badge = f"[{s.get('risk_level')}: {s.get('impact_category')}]"
        print(
            f"  Priority {s['priority']} {badge}: {s['old_ruleset']} ->"
            f" {s['new_ruleset']}{cnt}"
        )


if __name__ == '__main__':
  main(sys.argv[1:])
