#!/usr/bin/env python3
r"""Deterministic CLI parameter validator for the assured-workloads-basics skill.

Validates parameters for Assured Workloads V1 operations (create, list,
describe/get) before executing gcloud CLI or Python client library calls.

Usage examples:
  # Validate Create parameters
  python3 scripts/validate_params.py \
    --operation=create \
    --organization=123456789012 \
    --location=us-central1 \
    --display-name="FedRAMP-Moderate-Enclave" \
    --compliance-regime=DATA_BOUNDARY_FOR_FEDRAMP_MODERATE

  # Validate List parameters
  python3 scripts/validate_params.py \
    --operation=list \
    --organization=123456789012 \
    --location=us-central1

  # Validate Describe (Get) parameters
  python3 scripts/validate_params.py \
    --operation=describe \
    --organization=123456789012 \
    --location=us-central1 \
    --workload-id=9876543210
"""

import argparse
import json
import os
import re
import shlex
import sys
from typing import Any

_ORG_ID_RE = re.compile(r"^\d+$")
_DISPLAY_NAME_RE = re.compile(r"^[a-zA-Z0-9 -]{4,30}$")
_BILLING_ACCOUNT_RE = re.compile(r"^billingAccounts/[A-Za-z0-9-]+$")
_FOLDER_PARENT_RE = re.compile(r"^folders/\d+$")
_EXTERNAL_ID_RE = re.compile(r"^[a-zA-Z0-9_-]{1,63}$")
_WORKLOAD_ID_RE = re.compile(r"^[a-zA-Z0-9_-]+$")
_WORKLOAD_NAME_RE = re.compile(
    r"^organizations/(\d+)/locations/([a-z0-9-]+)/workloads/([a-zA-Z0-9_-]+)$"
)
_PROJECT_ID_RE = re.compile(r"^[a-z][a-z0-9-]{4,28}[a-z0-9]$")
_KEYRING_ID_RE = re.compile(r"^[a-zA-Z0-9_-]{1,63}$")
_ROTATION_PERIOD_RE = re.compile(r"^[1-9]\d*s$")
_ISO8601_TIME_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)
_LABEL_KEY_RE = re.compile(r"^[a-z][a-z0-9_-]{0,62}$")
_LABEL_VALUE_RE = re.compile(r"^[a-z0-9_-]{0,63}$")

METRICS_ENV_PREFIX = (
    'CLOUDSDK_METRICS_REQUEST_ATTRIBUTION="agent-skills/1.0'
    ' (skill:assured-workloads-basics)"'
)

US_LOCATIONS: frozenset[str] = frozenset({
    "us",
    "us-central1",
    "us-east1",
    "us-east4",
    "us-east5",
    "us-south1",
    "us-west1",
    "us-west2",
    "us-west3",
    "us-west4",
})

IL4_LOCATIONS: frozenset[str] = frozenset({
    "us",
    "us-central1",
    "us-east1",
    "us-east4",
    "us-west1",
    "us-west2",
    "us-west3",
    "us-west4",
})

IL5_LOCATIONS: frozenset[str] = frozenset({
    "us",
    "us-central1",
    "us-east4",
    "us-west1",
    "us-west2",
})

EU_LOCATIONS: frozenset[str] = frozenset({
    "europe",
    "eu",
    "europe-central2",
    "europe-north1",
    "europe-north2",
    "europe-southwest1",
    "europe-west1",
    "europe-west3",
    "europe-west4",
    "europe-west8",
    "europe-west9",
    "europe-west10",
    "europe-west12",
})

CA_LOCATIONS: frozenset[str] = frozenset({
    "ca",
    "canada",
    "northamerica-northeast1",
    "northamerica-northeast2",
})

AU_LOCATIONS: frozenset[str] = frozenset({
    "australia-southeast1",
    "australia-southeast2",
})

JP_LOCATIONS: frozenset[str] = frozenset({
    "asia-northeast1",
    "asia-northeast2",
})

ISR_LOCATIONS: frozenset[str] = frozenset({
    "me-west1",
})

KSA_LOCATIONS: frozenset[str] = frozenset({
    "me-central2",
})

CH_LOCATIONS: frozenset[str] = frozenset({
    "europe-west6",
})

OTHER_REGIONAL_LOCATIONS: frozenset[str] = frozenset({
    "africa-south1",
    "asia-east1",
    "asia-east2",
    "asia-northeast3",
    "asia-south1",
    "asia-south2",
    "asia-southeast1",
    "asia-southeast2",
    "europe-west2",
    "me-central1",
    "southamerica-east1",
    "southamerica-west1",
})

ALL_VALID_V1_LOCATIONS: frozenset[str] = (
    US_LOCATIONS
    | EU_LOCATIONS
    | CA_LOCATIONS
    | AU_LOCATIONS
    | JP_LOCATIONS
    | ISR_LOCATIONS
    | KSA_LOCATIONS
    | CH_LOCATIONS
    | OTHER_REGIONAL_LOCATIONS
)

# Authoritative mapping of all 45 V1 ComplianceRegime values to their allowed
# locations and modern recommended Data Boundary enum name.
REGIME_SPEC: dict[str, dict[str, Any]] = {
    # US Regimes (Modern & Legacy)
    "US_DATA_BOUNDARY_AND_SUPPORT": {
        "locations": US_LOCATIONS,
        "recommended": "US_DATA_BOUNDARY_AND_SUPPORT",
    },
    "US_REGIONAL_ACCESS": {
        "locations": US_LOCATIONS,
        "recommended": "US_DATA_BOUNDARY_AND_SUPPORT",
    },
    "DATA_BOUNDARY_FOR_FEDRAMP_MODERATE": {
        "locations": US_LOCATIONS,
        "recommended": "DATA_BOUNDARY_FOR_FEDRAMP_MODERATE",
    },
    "FEDRAMP_MODERATE": {
        "locations": US_LOCATIONS,
        "recommended": "DATA_BOUNDARY_FOR_FEDRAMP_MODERATE",
    },
    "DATA_BOUNDARY_FOR_FEDRAMP_HIGH": {
        "locations": US_LOCATIONS,
        "recommended": "DATA_BOUNDARY_FOR_FEDRAMP_HIGH",
    },
    "FEDRAMP_HIGH": {
        "locations": US_LOCATIONS,
        "recommended": "DATA_BOUNDARY_FOR_FEDRAMP_HIGH",
    },
    "DATA_BOUNDARY_FOR_IL2": {
        "locations": US_LOCATIONS,
        "recommended": "DATA_BOUNDARY_FOR_IL2",
    },
    "IL2": {
        "locations": US_LOCATIONS,
        "recommended": "DATA_BOUNDARY_FOR_IL2",
    },
    "DATA_BOUNDARY_FOR_IL4": {
        "locations": IL4_LOCATIONS,
        "recommended": "DATA_BOUNDARY_FOR_IL4",
    },
    "IL4": {
        "locations": IL4_LOCATIONS,
        "recommended": "DATA_BOUNDARY_FOR_IL4",
    },
    "DATA_BOUNDARY_FOR_IL5": {
        "locations": IL5_LOCATIONS,
        "recommended": "DATA_BOUNDARY_FOR_IL5",
    },
    "IL5": {
        "locations": IL5_LOCATIONS,
        "recommended": "DATA_BOUNDARY_FOR_IL5",
    },
    "DATA_BOUNDARY_FOR_ITAR": {
        "locations": US_LOCATIONS,
        "recommended": "DATA_BOUNDARY_FOR_ITAR",
    },
    "ITAR": {
        "locations": US_LOCATIONS,
        "recommended": "DATA_BOUNDARY_FOR_ITAR",
    },
    "DATA_BOUNDARY_FOR_CJIS": {
        "locations": US_LOCATIONS,
        "recommended": "DATA_BOUNDARY_FOR_CJIS",
    },
    "CJIS": {
        "locations": US_LOCATIONS,
        "recommended": "DATA_BOUNDARY_FOR_CJIS",
    },
    "DATA_BOUNDARY_FOR_IRS_PUBLICATION_1075": {
        "locations": US_LOCATIONS,
        "recommended": "DATA_BOUNDARY_FOR_IRS_PUBLICATION_1075",
    },
    "IRS_1075": {
        "locations": US_LOCATIONS,
        "recommended": "DATA_BOUNDARY_FOR_IRS_PUBLICATION_1075",
    },
    "US_DATA_BOUNDARY_FOR_HEALTHCARE_AND_LIFE_SCIENCES": {
        "locations": US_LOCATIONS,
        "recommended": "US_DATA_BOUNDARY_FOR_HEALTHCARE_AND_LIFE_SCIENCES",
    },
    "HEALTHCARE_AND_LIFE_SCIENCES_CONTROLS": {
        "locations": US_LOCATIONS,
        "recommended": "US_DATA_BOUNDARY_FOR_HEALTHCARE_AND_LIFE_SCIENCES",
    },
    "US_DATA_BOUNDARY_FOR_HEALTHCARE_AND_LIFE_SCIENCES_WITH_SUPPORT": {
        "locations": US_LOCATIONS,
        "recommended": (
            "US_DATA_BOUNDARY_FOR_HEALTHCARE_AND_LIFE_SCIENCES_WITH_SUPPORT"
        ),
    },
    "HEALTHCARE_AND_LIFE_SCIENCES_CONTROLS_US_SUPPORT": {
        "locations": US_LOCATIONS,
        "recommended": (
            "US_DATA_BOUNDARY_FOR_HEALTHCARE_AND_LIFE_SCIENCES_WITH_SUPPORT"
        ),
    },
    "HIPAA": {
        "locations": US_LOCATIONS,
        "recommended": "US_DATA_BOUNDARY_FOR_HEALTHCARE_AND_LIFE_SCIENCES",
        "deprecated": True,
    },
    "HITRUST": {
        "locations": US_LOCATIONS,
        "recommended": "US_DATA_BOUNDARY_FOR_HEALTHCARE_AND_LIFE_SCIENCES",
        "deprecated": True,
    },
    # EU & Switzerland Regimes
    "EU_DATA_BOUNDARY_AND_SUPPORT": {
        "locations": EU_LOCATIONS,
        "recommended": "EU_DATA_BOUNDARY_AND_SUPPORT",
    },
    "EU_REGIONS_AND_SUPPORT": {
        "locations": EU_LOCATIONS,
        "recommended": "EU_DATA_BOUNDARY_AND_SUPPORT",
    },
    "SWITZERLAND_DATA_BOUNDARY_WITH_ACCESS_JUSTIFICATIONS": {
        "locations": CH_LOCATIONS,
        "recommended": "SWITZERLAND_DATA_BOUNDARY_WITH_ACCESS_JUSTIFICATIONS",
    },
    # Canada Regimes
    "CANADA_DATA_BOUNDARY_AND_SUPPORT": {
        "locations": CA_LOCATIONS,
        "recommended": "CANADA_DATA_BOUNDARY_AND_SUPPORT",
    },
    "CA_REGIONS_AND_SUPPORT": {
        "locations": CA_LOCATIONS,
        "recommended": "CANADA_DATA_BOUNDARY_AND_SUPPORT",
    },
    "DATA_BOUNDARY_FOR_CANADA_PROTECTED_B": {
        "locations": CA_LOCATIONS,
        "recommended": "DATA_BOUNDARY_FOR_CANADA_PROTECTED_B",
    },
    "CA_PROTECTED_B": {
        "locations": CA_LOCATIONS,
        "recommended": "DATA_BOUNDARY_FOR_CANADA_PROTECTED_B",
    },
    "DATA_BOUNDARY_FOR_CANADA_CONTROLLED_GOODS": {
        "locations": CA_LOCATIONS,
        "recommended": "DATA_BOUNDARY_FOR_CANADA_CONTROLLED_GOODS",
    },
    "CANADA_CONTROLLED_GOODS": {
        "locations": CA_LOCATIONS,
        "recommended": "DATA_BOUNDARY_FOR_CANADA_CONTROLLED_GOODS",
    },
    # APAC & Middle East Regimes
    "AUSTRALIA_DATA_BOUNDARY_AND_SUPPORT": {
        "locations": AU_LOCATIONS,
        "recommended": "AUSTRALIA_DATA_BOUNDARY_AND_SUPPORT",
    },
    "AU_REGIONS_AND_US_SUPPORT": {
        "locations": AU_LOCATIONS,
        "recommended": "AUSTRALIA_DATA_BOUNDARY_AND_SUPPORT",
    },
    "JAPAN_DATA_BOUNDARY": {
        "locations": JP_LOCATIONS,
        "recommended": "JAPAN_DATA_BOUNDARY",
    },
    "JP_REGIONS_AND_SUPPORT": {
        "locations": JP_LOCATIONS,
        "recommended": "JAPAN_DATA_BOUNDARY",
    },
    "ISRAEL_DATA_BOUNDARY_AND_SUPPORT": {
        "locations": ISR_LOCATIONS,
        "recommended": "ISRAEL_DATA_BOUNDARY_AND_SUPPORT",
    },
    "ISR_REGIONS": {
        "locations": ISR_LOCATIONS,
        "recommended": "ISRAEL_DATA_BOUNDARY_AND_SUPPORT",
    },
    "ISR_REGIONS_AND_SUPPORT": {
        "locations": ISR_LOCATIONS,
        "recommended": "ISRAEL_DATA_BOUNDARY_AND_SUPPORT",
    },
    "KSA_DATA_BOUNDARY_WITH_ACCESS_JUSTIFICATIONS": {
        "locations": KSA_LOCATIONS,
        "recommended": "KSA_DATA_BOUNDARY_WITH_ACCESS_JUSTIFICATIONS",
    },
    "KSA_REGIONS_AND_SUPPORT_WITH_SOVEREIGNTY_CONTROLS": {
        "locations": KSA_LOCATIONS,
        "recommended": "KSA_DATA_BOUNDARY_WITH_ACCESS_JUSTIFICATIONS",
    },
    # Free Tier & Partner Regimes
    "REGIONAL_DATA_BOUNDARY": {
        "locations": ALL_VALID_V1_LOCATIONS,
        "recommended": "REGIONAL_DATA_BOUNDARY",
    },
    "REGIONAL_CONTROLS": {
        "locations": ALL_VALID_V1_LOCATIONS,
        "recommended": "REGIONAL_DATA_BOUNDARY",
    },
    "ASSURED_WORKLOADS_FOR_PARTNERS": {
        "locations": ALL_VALID_V1_LOCATIONS,
        "recommended": "ASSURED_WORKLOADS_FOR_PARTNERS",
    },
}

VALID_PARTNERS: frozenset[str] = frozenset({
    "LOCAL_CONTROLS_BY_S3NS",
    "SOVEREIGN_CONTROLS_BY_T_SYSTEMS",
    "SOVEREIGN_CONTROLS_BY_SIA_MINSAIT",
    "SOVEREIGN_CONTROLS_BY_PSN",
    "SOVEREIGN_CONTROLS_BY_CNTXT",
    "SOVEREIGN_CONTROLS_BY_CNTXT_NO_EKM",
    "SPAIN_DATA_BOUNDARY_BY_TELEFONICA",
})

# Per googlecloudsdk/command_lib/assured/flags.py, SIA/PSN/CNTXT partner
# workloads require --partner-services-billing-account.
PARTNERS_REQUIRING_BILLING_ACCOUNT: frozenset[str] = frozenset({
    "SOVEREIGN_CONTROLS_BY_SIA_MINSAIT",
    "SOVEREIGN_CONTROLS_BY_PSN",
    "SOVEREIGN_CONTROLS_BY_CNTXT",
    "SOVEREIGN_CONTROLS_BY_CNTXT_NO_EKM",
})

# Partner-specific sovereign controls are bound to specific regions per official
# documentation (https://cloud.google.com/sovereign-controls-by-partners/docs/locations).
PARTNER_LOCATIONS: dict[str, frozenset[str]] = {
    "LOCAL_CONTROLS_BY_S3NS": frozenset({
        "europe-west1",
        "europe-west4",
        "europe-west9",
    }),
    "SOVEREIGN_CONTROLS_BY_T_SYSTEMS": frozenset({"europe-west3"}),
    "SOVEREIGN_CONTROLS_BY_SIA_MINSAIT": frozenset({"europe-southwest1"}),
    "SPAIN_DATA_BOUNDARY_BY_TELEFONICA": frozenset({"europe-southwest1"}),
    "SOVEREIGN_CONTROLS_BY_PSN": frozenset({
        "europe-west8",
        "europe-west12",
    }),
    "SOVEREIGN_CONTROLS_BY_CNTXT": frozenset({"me-central2"}),
    "SOVEREIGN_CONTROLS_BY_CNTXT_NO_EKM": frozenset({"me-central2"}),
}

VALID_RESOURCE_SETTINGS_KEYS: frozenset[str] = frozenset({
    "consumer-project-id",
    "consumer-project-name",
    "encryption-keys-project-id",
    "encryption-keys-project-name",
    "keyring-id",
})

KMS_DEPENDENT_RESOURCE_SETTINGS_KEYS: frozenset[str] = frozenset({
    "encryption-keys-project-id",
    "encryption-keys-project-name",
    "keyring-id",
})

VALID_RESTRICTION_TYPES: frozenset[str] = frozenset({
    "ALLOW_COMPLIANT_RESOURCES",
    "APPEND_COMPLIANT_RESOURCES",
    "ALLOW_ALL_GCP_RESOURCES",
})


def normalize_org_id(organization: str | None) -> str:
  """Strips 'organizations/' prefix if present and validates numeric Org ID."""
  if not organization or not organization.strip():
    raise ValueError("Missing required '--organization' parameter.")
  clean_org = organization.strip()
  if clean_org.startswith("organizations/"):
    clean_org = clean_org[len("organizations/") :].strip()
  if not _ORG_ID_RE.fullmatch(clean_org):
    raise ValueError(
        f"Invalid organization ID '{organization}'. Expected a numeric"
        " Google Cloud Organization ID (e.g., '123456789012')."
    )
  return clean_org


def validate_location(location: str | None) -> str:
  """Validates that the location is a valid regional/multi-regional V1 location."""
  if not location or not location.strip():
    raise ValueError("Missing required '--location' parameter.")
  clean_loc = location.strip().lower()
  if clean_loc == "global":
    raise ValueError(
        "Invalid location 'global'. Assured Workloads V1 requires a regional"
        " or multi-regional location (e.g., 'us-central1', 'us', 'eu',"
        " 'europe-west3', 'northamerica-northeast1')."
    )
  if clean_loc not in ALL_VALID_V1_LOCATIONS:
    raise ValueError(
        f"Unsupported Assured Workloads V1 location '{location}'. Supported"
        f" locations: {sorted(ALL_VALID_V1_LOCATIONS)}"
    )
  return clean_loc


def resolve_workload_resource_name(
    workload_id_or_name: str | None,
    organization: str | None = None,
    location: str | None = None,
) -> tuple[str, str, str, str]:
  """Resolves and validates (workload_name, org_id, location, workload_id)."""
  if not workload_id_or_name or not workload_id_or_name.strip():
    raise ValueError("Missing required '--workload-id' parameter.")
  candidate = workload_id_or_name.strip()
  match = _WORKLOAD_NAME_RE.fullmatch(candidate)
  if match:
    org_id, loc, w_id = match.group(1), match.group(2), match.group(3)
    clean_loc = validate_location(loc)
    if organization:
      explicit_org = normalize_org_id(organization)
      if explicit_org != org_id:
        raise ValueError(
            f"Organization ID mismatch: '--organization={explicit_org}' does"
            f" not match resource name organization '{org_id}'."
        )
    if location:
      explicit_loc = validate_location(location)
      if explicit_loc != clean_loc:
        raise ValueError(
            f"Location mismatch: '--location={explicit_loc}' does not match"
            f" resource name location '{clean_loc}'."
        )
    full_name = (
        f"organizations/{org_id}/locations/{clean_loc}/workloads/{w_id}"
    )
    return full_name, org_id, clean_loc, w_id

  clean_org = normalize_org_id(organization)
  clean_loc = validate_location(location)
  if not _WORKLOAD_ID_RE.fullmatch(candidate):
    raise ValueError(
        f"Invalid workload ID '{workload_id_or_name}'. Expected workload ID or"
        " full resource name"
        " 'organizations/<ORG>/locations/<LOC>/workloads/<ID>'."
    )
  full_name = (
      f"organizations/{clean_org}/locations/{clean_loc}/workloads/{candidate}"
  )
  return full_name, clean_org, clean_loc, candidate


def _parse_key_value_csv(raw_csv: str, flag_name: str) -> dict[str, str]:
  """Parses a comma-separated KEY=VALUE string into a dictionary."""
  parsed: dict[str, str] = {}
  for item in raw_csv.split(","):
    entry = item.strip()
    if not entry:
      continue
    if "=" not in entry:
      raise ValueError(
          f"Invalid '{flag_name}' entry '{entry}'. Expected comma-separated"
          " KEY=VALUE pairs."
      )
    key, val = entry.split("=", 1)
    clean_key = key.strip()
    clean_val = val.strip()
    if not clean_key:
      raise ValueError(f"Empty key in '{flag_name}' entry '{entry}'.")
    parsed[clean_key] = clean_val
  if not parsed:
    raise ValueError(f"Flag '{flag_name}' cannot be empty when specified.")
  return parsed


def validate_kms_and_resource_settings(
    resource_settings: str | None,
    next_rotation_time: str | None,
    rotation_period: str | None,
) -> tuple[dict[str, str] | None, str | None, str | None]:
  """Validates KMS rotation flags and custom resource-settings."""
  clean_next_rotation: str | None = None
  clean_rotation_period: str | None = None

  if bool(next_rotation_time) != bool(rotation_period):
    raise ValueError(
        "Both '--next-rotation-time' and '--rotation-period' must be specified"
        " together when configuring KMS key rotation settings."
    )

  if next_rotation_time and rotation_period:
    clean_next_rotation = next_rotation_time.strip()
    if not _ISO8601_TIME_RE.fullmatch(clean_next_rotation):
      raise ValueError(
          f"Invalid '--next-rotation-time' value '{clean_next_rotation}'."
          " Expected RFC 3339 / ISO-8601 timestamp (e.g.,"
          " '2026-12-30T10:15:30.00Z')."
      )
    clean_rotation_period = rotation_period.strip()
    if not _ROTATION_PERIOD_RE.fullmatch(clean_rotation_period):
      raise ValueError(
          f"Invalid '--rotation-period' value '{clean_rotation_period}'."
          " Expected duration in seconds ending with 's' (e.g., '172800s' or"
          " '7776000s')."
      )

  if not resource_settings:
    return None, clean_next_rotation, clean_rotation_period

  parsed_settings = _parse_key_value_csv(
      resource_settings, "--resource-settings"
  )
  unknown_keys = set(parsed_settings.keys()) - VALID_RESOURCE_SETTINGS_KEYS
  if unknown_keys:
    raise ValueError(
        f"Unsupported key(s) in '--resource-settings': {sorted(unknown_keys)}."
        f" Supported keys: {sorted(VALID_RESOURCE_SETTINGS_KEYS)}"
    )

  kms_keys_used = (
      set(parsed_settings.keys()) & KMS_DEPENDENT_RESOURCE_SETTINGS_KEYS
  )
  if kms_keys_used and not (clean_next_rotation and clean_rotation_period):
    raise ValueError(
        f"Resource settings {sorted(kms_keys_used)} can only be specified when"
        " KMS settings ('--next-rotation-time' and '--rotation-period') are"
        " provided."
    )

  for proj_id_key in ("consumer-project-id", "encryption-keys-project-id"):
    if proj_id_key in parsed_settings:
      val = parsed_settings[proj_id_key]
      if not _PROJECT_ID_RE.fullmatch(val):
        raise ValueError(
            f"Invalid '{proj_id_key}' value '{val}' in '--resource-settings'."
            " Must be 6 to 30 lowercase letters, digits, or hyphens, starting"
            " with a letter."
        )

  for proj_name_key in (
      "consumer-project-name",
      "encryption-keys-project-name",
  ):
    if proj_name_key in parsed_settings:
      val = parsed_settings[proj_name_key]
      if not _DISPLAY_NAME_RE.fullmatch(val):
        raise ValueError(
            f"Invalid '{proj_name_key}' value '{val}' in '--resource-settings'."
            " Must be 4 to 30 characters ([a-zA-Z0-9 -])."
        )

  if "keyring-id" in parsed_settings:
    kr_val = parsed_settings["keyring-id"]
    if not _KEYRING_ID_RE.fullmatch(kr_val):
      raise ValueError(
          f"Invalid 'keyring-id' value '{kr_val}' in '--resource-settings'."
          " Must be 1 to 63 alphanumeric, underscore, or hyphen characters."
      )

  return parsed_settings, clean_next_rotation, clean_rotation_period


def validate_labels(labels: str | None) -> dict[str, str] | None:
  """Validates --labels KEY=VALUE pairs against Google Cloud label rules."""
  if labels is None:
    return None
  if not labels.strip():
    raise ValueError(
        "Invalid '--labels' value: at least one KEY=VALUE pair must be"
        " specified when '--labels' is provided."
    )
  parsed = _parse_key_value_csv(labels, "--labels")
  for k, v in parsed.items():
    if not _LABEL_KEY_RE.fullmatch(k):
      raise ValueError(
          f"Invalid label key '{k}'. Label keys must start with a lowercase"
          " letter and contain only lowercase letters, digits, underscores, or"
          " hyphens (max 63 chars)."
      )
    if not _LABEL_VALUE_RE.fullmatch(v):
      raise ValueError(
          f"Invalid label value '{v}' for key '{k}'. Label values may contain"
          " only lowercase letters, digits, underscores, or hyphens (max 63"
          " chars)."
      )
  return parsed


def _get_sibling_script_path(script_filename: str) -> str:
  """Returns the path to a sibling script in scripts/, relative to CWD when under CWD."""
  script_dir = os.path.dirname(os.path.abspath(__file__))
  abs_target = os.path.join(script_dir, script_filename)
  try:
    rel_target = os.path.relpath(abs_target)
    if not rel_target.startswith(".."):
      return rel_target
  except ValueError:
    pass
  return abs_target


def validate_create_params(
    organization: str | None,
    location: str | None,
    display_name: str | None,
    compliance_regime: str | None,
    billing_account: str | None = None,
    provisioned_resources_parent: str | None = None,
    restriction_type: str = "ALLOW_COMPLIANT_RESOURCES",
    enable_sovereign_controls: bool = False,
    partner: str | None = None,
    partner_permissions: str | None = None,
    partner_services_billing_account: str | None = None,
    resource_settings: str | None = None,
    next_rotation_time: str | None = None,
    rotation_period: str | None = None,
    labels: str | None = None,
    external_identifier: str | None = None,
) -> dict[str, Any]:
  """Validates parameters for creating an Assured Workloads workload and builds commands."""
  clean_org = normalize_org_id(organization)
  clean_loc = validate_location(location)

  if not display_name or not display_name.strip():
    raise ValueError("Missing required '--display-name' for workload creation.")
  clean_display_name = display_name.strip()
  if not _DISPLAY_NAME_RE.fullmatch(clean_display_name):
    raise ValueError(
        f"Invalid display name '{clean_display_name}'. Must be 4 to 30"
        " characters and contain only alphanumeric characters, spaces, and"
        " hyphens ([a-zA-Z0-9 -])."
    )

  if not compliance_regime or not compliance_regime.strip():
    raise ValueError(
        "Missing required '--compliance-regime' for workload creation."
    )
  clean_regime = compliance_regime.strip().upper().replace("-", "_")
  if clean_regime.startswith("COMPLIANCE_REGIME_"):
    clean_regime = clean_regime[len("COMPLIANCE_REGIME_") :]

  if clean_regime not in REGIME_SPEC:
    raise ValueError(
        f"Unsupported compliance regime '{compliance_regime}'. Valid V1"
        f" regimes: {sorted(REGIME_SPEC.keys())}"
    )

  spec = REGIME_SPEC[clean_regime]
  allowed_locs: frozenset[str] = spec["locations"]
  if clean_loc not in allowed_locs:
    raise ValueError(
        f"Location '{clean_loc}' is incompatible with compliance regime"
        f" '{clean_regime}'. Allowed locations for '{clean_regime}':"
        f" {sorted(allowed_locs)}"
    )

  warnings: list[str] = []
  recommended_regime = spec["recommended"]
  if spec.get("deprecated"):
    warnings.append(
        f"Compliance regime '{clean_regime}' is deprecated. Consider using"
        f" '{recommended_regime}' or"
        " 'US_DATA_BOUNDARY_FOR_HEALTHCARE_AND_LIFE_SCIENCES_WITH_SUPPORT'"
        " instead."
    )
  elif recommended_regime != clean_regime:
    warnings.append(
        f"Compliance regime '{clean_regime}' is a legacy alias. The modern"
        f" Data Boundary enum is '{recommended_regime}' (both are accepted by"
        " gcloud)."
    )

  clean_partner: str | None = None
  clean_partner_permissions: dict[str, bool] | None = None
  clean_partner_billing: str | None = None

  if clean_regime == "ASSURED_WORKLOADS_FOR_PARTNERS":
    if not partner or not partner.strip():
      raise ValueError(
          "Compliance regime 'ASSURED_WORKLOADS_FOR_PARTNERS' requires"
          f" '--partner' to be specified. Valid partners: {sorted(VALID_PARTNERS)}"
      )
    clean_partner = partner.strip().upper().replace("-", "_")
    if clean_partner not in VALID_PARTNERS:
      raise ValueError(
          f"Invalid partner '{partner}'. Valid partners:"
          f" {sorted(VALID_PARTNERS)}"
      )
    if (
        clean_partner in PARTNERS_REQUIRING_BILLING_ACCOUNT
        and not partner_services_billing_account
    ):
      raise ValueError(
          f"Partner '{clean_partner}' requires"
          " '--partner-services-billing-account=billingAccounts/<ID>'."
      )
    if clean_partner in PARTNER_LOCATIONS:
      allowed_partner_locs = PARTNER_LOCATIONS[clean_partner]
      if clean_loc not in allowed_partner_locs:
        raise ValueError(
            f"Partner '{clean_partner}' requires '--location' to be one of"
            f" {sorted(allowed_partner_locs)}, but got '{clean_loc}'."
        )
  elif partner or partner_permissions or partner_services_billing_account:
    raise ValueError(
        "Partner flags ('--partner', '--partner-permissions',"
        " '--partner-services-billing-account') can only be used when"
        " '--compliance-regime=ASSURED_WORKLOADS_FOR_PARTNERS'."
    )

  if partner_permissions:
    raw_perms = _parse_key_value_csv(
        partner_permissions, "--partner-permissions"
    )
    if set(raw_perms.keys()) != {"data-logs-viewer"}:
      raise ValueError(
          "Invalid '--partner-permissions' key(s)"
          f" {sorted(raw_perms.keys())}. Only 'data-logs-viewer=true|false' is"
          " supported."
      )
    val_lower = raw_perms["data-logs-viewer"].lower()
    if val_lower not in ("true", "false"):
      raise ValueError(
          "Invalid '--partner-permissions' value for 'data-logs-viewer':"
          f" '{raw_perms['data-logs-viewer']}'. Expected 'true' or 'false'."
      )
    clean_partner_permissions = {"data-logs-viewer": val_lower == "true"}

  if partner_services_billing_account:
    clean_partner_billing = partner_services_billing_account.strip()
    if not _BILLING_ACCOUNT_RE.fullmatch(clean_partner_billing):
      raise ValueError(
          "Invalid '--partner-services-billing-account' format"
          f" '{partner_services_billing_account}'. Expected"
          " 'billingAccounts/<BILLING_ACCOUNT_ID>'."
      )

  if not billing_account or not billing_account.strip():
    raise ValueError(
        "Missing required '--billing-account' for V1 workload creation"
        " ('gcloud assured workloads create' requires"
        " '--billing-account=billingAccounts/<BILLING_ACCOUNT_ID>')."
    )
  clean_billing = billing_account.strip()
  if not _BILLING_ACCOUNT_RE.fullmatch(clean_billing):
    raise ValueError(
        f"Invalid billing account format '{billing_account}'. Expected"
        " 'billingAccounts/<BILLING_ACCOUNT_ID>' (e.g.,"
        " 'billingAccounts/012345-6789AB-CDEF01')."
    )

  clean_parent: str | None = None
  if provisioned_resources_parent:
    clean_parent = provisioned_resources_parent.strip()
    if clean_parent.startswith("projects/"):
      raise ValueError(
          f"Invalid '--provisioned-resources-parent' value '{clean_parent}'."
          " Assured Workloads V1 creates a new workload folder under an"
          " organization or an existing parent folder ('folders/<FOLDER_ID>'),"
          " not a project."
      )
    if not _FOLDER_PARENT_RE.fullmatch(clean_parent):
      raise ValueError(
          f"Invalid '--provisioned-resources-parent' format '{clean_parent}'."
          " Expected 'folders/<FOLDER_ID>' (e.g., 'folders/123456789012')."
      )

  (
      clean_resource_settings,
      clean_next_rotation,
      clean_rotation_period,
  ) = validate_kms_and_resource_settings(
      resource_settings=resource_settings,
      next_rotation_time=next_rotation_time,
      rotation_period=rotation_period,
  )

  clean_labels = validate_labels(labels)

  clean_external_id: str | None = None
  if external_identifier:
    clean_external_id = external_identifier.strip()
    if not _EXTERNAL_ID_RE.fullmatch(clean_external_id):
      raise ValueError(
          f"Invalid '--external-identifier' value '{clean_external_id}'. Must"
          " be 1-63 alphanumeric, underscore, or hyphen characters."
      )

  clean_restriction = restriction_type.strip().upper().replace("-", "_")
  if clean_restriction not in VALID_RESTRICTION_TYPES:
    raise ValueError(
        f"Invalid '--restriction-type' value '{restriction_type}'. Valid"
        f" values: {sorted(VALID_RESTRICTION_TYPES)}"
    )

  # Build Phase 1 gcloud assured workloads create command
  cmd_parts = [
      METRICS_ENV_PREFIX,
      "gcloud assured workloads create",
      f"--organization={shlex.quote(clean_org)}",
      f"--location={shlex.quote(clean_loc)}",
      f"--display-name={shlex.quote(clean_display_name)}",
      f"--compliance-regime={shlex.quote(clean_regime)}",
  ]
  if clean_billing:
    cmd_parts.append(f"--billing-account={shlex.quote(clean_billing)}")
  if clean_parent:
    cmd_parts.append(
        f"--provisioned-resources-parent={shlex.quote(clean_parent)}"
    )
  if enable_sovereign_controls:
    cmd_parts.append("--enable-sovereign-controls")
  if clean_partner:
    cmd_parts.append(f"--partner={shlex.quote(clean_partner)}")
  if clean_partner_permissions is not None:
    perm_val = (
        "true" if clean_partner_permissions["data-logs-viewer"] else "false"
    )
    cmd_parts.append(f"--partner-permissions=data-logs-viewer={perm_val}")
  if clean_partner_billing:
    cmd_parts.append(
        f"--partner-services-billing-account={shlex.quote(clean_partner_billing)}"
    )
  if clean_next_rotation and clean_rotation_period:
    cmd_parts.append(f"--next-rotation-time={shlex.quote(clean_next_rotation)}")
    cmd_parts.append(f"--rotation-period={shlex.quote(clean_rotation_period)}")
  if clean_resource_settings:
    settings_csv = ",".join(
        f"{k}={v}" for k, v in clean_resource_settings.items()
    )
    cmd_parts.append(f"--resource-settings={shlex.quote(settings_csv)}")
  if clean_labels:
    labels_csv = ",".join(f"{k}={v}" for k, v in clean_labels.items())
    cmd_parts.append(f"--labels={shlex.quote(labels_csv)}")
  if clean_external_id:
    cmd_parts.append(f"--external-identifier={shlex.quote(clean_external_id)}")
  cmd_parts.append("--format=json")
  phase1_create_cmd = " \\\n  ".join(cmd_parts)

  phase2_describe_cmd = (
      f"{METRICS_ENV_PREFIX} \\\n"
      "  gcloud assured workloads describe <WORKLOAD_ID> \\\n"
      f"  --organization={shlex.quote(clean_org)} \\\n"
      f"  --location={shlex.quote(clean_loc)} \\\n"
      '  --format="json(name,displayName,resources,compliantButDisallowedServices)"'
  )

  restrict_script_path = _get_sibling_script_path(
      "restrict_allowed_resources.py"
  )
  phase2_required = clean_regime not in (
      "FEDRAMP_MODERATE",
      "DATA_BOUNDARY_FOR_FEDRAMP_MODERATE",
  )
  phase2_restrict_cmd = (
      f"python3 {shlex.quote(restrict_script_path)} \\\n"
      f"  --organization={shlex.quote(clean_org)} \\\n"
      f"  --location={shlex.quote(clean_loc)} \\\n"
      "  --workload-id=<WORKLOAD_ID> \\\n"
      f"  --restriction-type={shlex.quote(clean_restriction)} \\\n"
      "  --poll-timeout-seconds=300 \\\n"
      "  --poll-interval-seconds=15"
  )

  return {
      "valid": True,
      "operation": "create",
      "normalizedParams": {
          "organization": clean_org,
          "location": clean_loc,
          "displayName": clean_display_name,
          "complianceRegime": clean_regime,
          "recommendedComplianceRegime": recommended_regime,
          "billingAccount": clean_billing,
          "provisionedResourcesParent": clean_parent,
          "enableSovereignControls": enable_sovereign_controls,
          "partner": clean_partner,
          "partnerPermissions": clean_partner_permissions,
          "partnerServicesBillingAccount": clean_partner_billing,
          "nextRotationTime": clean_next_rotation,
          "rotationPeriod": clean_rotation_period,
          "resourceSettings": clean_resource_settings,
          "labels": clean_labels,
          "externalIdentifier": clean_external_id,
          "restrictionType": clean_restriction,
      },
      "warnings": warnings,
      "phase2Required": phase2_required,
      "phase1CreateCommand": phase1_create_cmd,
      "phase2DescribeCommand": phase2_describe_cmd,
      "phase2RestrictCommand": phase2_restrict_cmd,
      "consoleUrl": (
          "https://console.cloud.google.com/compliance/assuredworkloads"
          f"?organizationId={clean_org}"
      ),
  }


def validate_list_params(
    organization: str | None,
    location: str | None,
    limit: int | None = None,
    page_size: int | None = None,
    filter_expr: str | None = None,
) -> dict[str, Any]:
  """Validates parameters for listing Assured Workloads in an org/location."""
  clean_org = normalize_org_id(organization)
  clean_loc = validate_location(location)

  if limit is not None and limit < 1:
    raise ValueError(
        f"Invalid '--limit' value '{limit}'. Must be a positive integer (>= 1)."
    )
  if page_size is not None and page_size < 1:
    raise ValueError(
        f"Invalid '--page-size' value '{page_size}'. Must be a positive"
        " integer (>= 1)."
    )

  clean_filter = filter_expr.strip() if filter_expr and filter_expr.strip() else None

  cmd_parts = [
      METRICS_ENV_PREFIX,
      "gcloud assured workloads list",
      f"--organization={shlex.quote(clean_org)}",
      f"--location={shlex.quote(clean_loc)}",
  ]
  if limit is not None:
    cmd_parts.append(f"--limit={limit}")
  if page_size is not None:
    cmd_parts.append(f"--page-size={page_size}")
  if clean_filter:
    cmd_parts.append(f"--filter={shlex.quote(clean_filter)}")
  cmd_parts.append("--format=json")
  list_cmd = " \\\n  ".join(cmd_parts)

  return {
      "valid": True,
      "operation": "list",
      "normalizedParams": {
          "organization": clean_org,
          "location": clean_loc,
          "parent": f"organizations/{clean_org}/locations/{clean_loc}",
          "limit": limit,
          "pageSize": page_size,
          "filter": clean_filter,
      },
      "warnings": [],
      "listCommand": list_cmd,
      "consoleUrl": (
          "https://console.cloud.google.com/compliance/assuredworkloads"
          f"?organizationId={clean_org}"
      ),
  }


def validate_describe_params(
    workload_id: str | None,
    organization: str | None = None,
    location: str | None = None,
) -> dict[str, Any]:
  """Validates parameters for describing (getting) an Assured Workloads workload."""
  workload_name, clean_org, clean_loc, clean_w_id = (
      resolve_workload_resource_name(
          workload_id_or_name=workload_id,
          organization=organization,
          location=location,
      )
  )

  describe_cmd = (
      f"{METRICS_ENV_PREFIX} \\\n"
      f"  gcloud assured workloads describe {shlex.quote(clean_w_id)} \\\n"
      f"  --organization={shlex.quote(clean_org)} \\\n"
      f"  --location={shlex.quote(clean_loc)} \\\n"
      "  --format=json"
  )

  return {
      "valid": True,
      "operation": "describe",
      "normalizedParams": {
          "workloadName": workload_name,
          "workloadId": clean_w_id,
          "organization": clean_org,
          "location": clean_loc,
      },
      "warnings": [],
      "describeCommand": describe_cmd,
      "consoleUrl": (
          "https://console.cloud.google.com/compliance/assuredworkloads"
          f"?organizationId={clean_org}"
      ),
  }


def validate_delete_params(
    workload_id: str | None,
    organization: str | None = None,
    location: str | None = None,
    etag: str | None = None,
) -> dict[str, Any]:
  """Validates parameters for deleting an Assured Workloads workload."""
  workload_name, clean_org, clean_loc, clean_w_id = (
      resolve_workload_resource_name(
          workload_id_or_name=workload_id,
          organization=organization,
          location=location,
      )
  )

  clean_etag = None
  if etag is not None:
    clean_etag = etag.strip()
    if not clean_etag:
      raise ValueError(
          "Invalid '--etag' value: etag cannot be an empty string when"
          " specified."
      )

  pre_delete_describe_cmd = (
      f"{METRICS_ENV_PREFIX} \\\n"
      f"  gcloud assured workloads describe {shlex.quote(clean_w_id)} \\\n"
      f"  --organization={shlex.quote(clean_org)} \\\n"
      f"  --location={shlex.quote(clean_loc)} \\\n"
      '  --format="json(name,displayName,etag,resources)"'
  )

  cmd_parts = [
      METRICS_ENV_PREFIX,
      f"gcloud assured workloads delete {shlex.quote(clean_w_id)}",
      f"--organization={shlex.quote(clean_org)}",
      f"--location={shlex.quote(clean_loc)}",
  ]
  if clean_etag:
    cmd_parts.append(f"--etag={shlex.quote(clean_etag)}")
  cmd_parts.append("--quiet")
  delete_cmd = " \\\n  ".join(cmd_parts)

  return {
      "valid": True,
      "operation": "delete",
      "normalizedParams": {
          "workloadName": workload_name,
          "workloadId": clean_w_id,
          "organization": clean_org,
          "location": clean_loc,
          "etag": clean_etag,
      },
      "warnings": [],
      "preDeleteDescribeCommand": pre_delete_describe_cmd,
      "deleteCommand": delete_cmd,
      "consoleUrl": (
          "https://console.cloud.google.com/compliance/assuredworkloads"
          f"?organizationId={clean_org}"
      ),
  }


def validate_update_params(
    workload_id: str | None,
    organization: str | None = None,
    location: str | None = None,
    display_name: str | None = None,
    labels: str | None = None,
    violation_notifications_enabled: str | None = None,
    etag: str | None = None,
) -> dict[str, Any]:
  """Validates parameters for updating an Assured Workloads workload (V1 metadata/settings)."""
  workload_name, clean_org, clean_loc, clean_w_id = (
      resolve_workload_resource_name(
          workload_id_or_name=workload_id,
          organization=organization,
          location=location,
      )
  )

  clean_display_name: str | None = None
  if display_name is not None:
    clean_display_name = display_name.strip()
    if not _DISPLAY_NAME_RE.fullmatch(clean_display_name):
      raise ValueError(
          f"Invalid display name '{clean_display_name}'. Must be 4 to 30"
          " characters and contain only alphanumeric characters, spaces, and"
          " hyphens ([a-zA-Z0-9 -])."
      )
  clean_labels = validate_labels(labels)

  clean_violation_notifications: bool | None = None
  if violation_notifications_enabled is not None:
    raw_vn = violation_notifications_enabled.strip().lower()
    if raw_vn not in ("true", "false"):
      raise ValueError(
          "Invalid '--violation-notifications-enabled' value"
          f" '{violation_notifications_enabled}'. Must be 'true' or 'false'."
      )
    clean_violation_notifications = raw_vn == "true"

  clean_etag = None
  if etag is not None:
    clean_etag = etag.strip()
    if not clean_etag:
      raise ValueError(
          "Invalid '--etag' value: etag cannot be an empty string when"
          " specified."
      )

  if (
      clean_display_name is None
      and clean_labels is None
      and clean_violation_notifications is None
  ):
    raise ValueError(
        "At least one updatable V1 field must be specified for"
        " '--operation=update': '--display-name', '--labels', or"
        " '--violation-notifications-enabled'."
    )

  pre_update_describe_cmd = (
      f"{METRICS_ENV_PREFIX} \\\n"
      f"  gcloud assured workloads describe {shlex.quote(clean_w_id)} \\\n"
      f"  --organization={shlex.quote(clean_org)} \\\n"
      f"  --location={shlex.quote(clean_loc)} \\\n"
      '  --format="json(name,displayName,labels,violationNotificationsEnabled,etag)"'
  )

  cmd_parts = [
      METRICS_ENV_PREFIX,
      f"gcloud assured workloads update {shlex.quote(clean_w_id)}",
      f"--organization={shlex.quote(clean_org)}",
      f"--location={shlex.quote(clean_loc)}",
  ]
  if clean_display_name is not None:
    cmd_parts.append(f"--display-name={shlex.quote(clean_display_name)}")
  if clean_labels is not None:
    labels_csv = ",".join(f"{k}={v}" for k, v in clean_labels.items())
    cmd_parts.append(f"--labels={shlex.quote(labels_csv)}")
  if clean_violation_notifications is not None:
    vn_str = "true" if clean_violation_notifications else "false"
    cmd_parts.append(f"--violation-notifications-enabled={vn_str}")
  if clean_etag is not None:
    cmd_parts.append(f"--etag={shlex.quote(clean_etag)}")
  cmd_parts.append("--format=json")
  update_cmd = " \\\n  ".join(cmd_parts)

  updates_script_path = _get_sibling_script_path("manage_workload_updates.py")
  list_updates_cmd = (
      f"python3 {shlex.quote(updates_script_path)} \\\n"
      "  --action=list \\\n"
      f"  --organization={shlex.quote(clean_org)} \\\n"
      f"  --location={shlex.quote(clean_loc)} \\\n"
      f"  --workload-id={shlex.quote(clean_w_id)}"
  )
  apply_update_cmd_template = (
      f"python3 {shlex.quote(updates_script_path)} \\\n"
      "  --action=apply \\\n"
      f"  --organization={shlex.quote(clean_org)} \\\n"
      f"  --location={shlex.quote(clean_loc)} \\\n"
      f"  --workload-id={shlex.quote(clean_w_id)} \\\n"
      "  --update-id=<UPDATE_ID>"
  )

  return {
      "valid": True,
      "operation": "update",
      "normalizedParams": {
          "workloadName": workload_name,
          "workloadId": clean_w_id,
          "organization": clean_org,
          "location": clean_loc,
          "displayName": clean_display_name,
          "labels": clean_labels,
          "violationNotificationsEnabled": clean_violation_notifications,
          "etag": clean_etag,
      },
      "warnings": [],
      "preUpdateDescribeCommand": pre_update_describe_cmd,
      "updateCommand": update_cmd,
      "listUpdatesCommand": list_updates_cmd,
      "applyUpdateCommandTemplate": apply_update_cmd_template,
      "consoleUrl": (
          "https://console.cloud.google.com/compliance/assuredworkloads"
          f"?organizationId={clean_org}"
      ),
  }


_UPDATE_RESOURCE_NAME_RE = re.compile(
    r"^organizations/(\d+)/locations/([a-z0-9-]+)/workloads/([a-zA-Z0-9_-]+)/updates/([a-zA-Z0-9_-]+)$"
)


def validate_list_updates_params(
    workload_id: str | None,
    organization: str | None = None,
    location: str | None = None,
    enable_compliance_updates: bool = False,
) -> dict[str, Any]:
  """Validates parameters for listing V1 compliance configuration updates."""
  workload_name, clean_org, clean_loc, clean_w_id = (
      resolve_workload_resource_name(
          workload_id_or_name=workload_id,
          organization=organization,
          location=location,
      )
  )
  updates_script_path = _get_sibling_script_path("manage_workload_updates.py")
  cmd_parts = [
      f"python3 {shlex.quote(updates_script_path)}",
      "--action=list",
      f"--organization={shlex.quote(clean_org)}",
      f"--location={shlex.quote(clean_loc)}",
      f"--workload-id={shlex.quote(clean_w_id)}",
  ]
  if enable_compliance_updates:
    cmd_parts.append("--enable-compliance-updates")
  list_updates_cmd = " \\\n  ".join(cmd_parts)

  return {
      "valid": True,
      "operation": "list-updates",
      "normalizedParams": {
          "workloadName": workload_name,
          "workloadId": clean_w_id,
          "organization": clean_org,
          "location": clean_loc,
          "enableComplianceUpdates": enable_compliance_updates,
      },
      "warnings": [],
      "listUpdatesCommand": list_updates_cmd,
      "consoleUrl": (
          "https://console.cloud.google.com/compliance/assuredworkloads"
          f"?organizationId={clean_org}"
      ),
  }


def validate_apply_update_params(
    workload_id: str | None = None,
    organization: str | None = None,
    location: str | None = None,
    update_id: str | None = None,
) -> dict[str, Any]:
  """Validates parameters for applying one, multiple, or ALL V1 compliance configuration updates."""
  if not update_id or not update_id.strip():
    raise ValueError(
        "Missing required '--update-id' for '--operation=apply-update'. Pass a"
        " specific update ID, comma-separated update IDs, or '--update-id=ALL'."
    )
  raw_tokens = [t.strip() for t in update_id.split(",") if t.strip()]
  if not raw_tokens:
    raise ValueError(
        "Missing required '--update-id' for '--operation=apply-update'."
    )

  inferred_org: str | None = None
  inferred_loc: str | None = None
  inferred_wid: str | None = None
  for tok in raw_tokens:
    u_match = _UPDATE_RESOURCE_NAME_RE.fullmatch(tok)
    if u_match:
      u_org, u_loc, u_wid = (
          u_match.group(1),
          u_match.group(2),
          u_match.group(3),
      )
      if u_loc == "global":
        raise ValueError(
            "Invalid location 'global' in update resource name. Assured"
            " Workloads V1 requires a regional or multi-regional location."
        )
      if inferred_org and inferred_org != u_org:
        raise ValueError(
            "All update resource names in '--update-id' must belong to the"
            " same organization."
        )
      if inferred_loc and inferred_loc != u_loc:
        raise ValueError(
            "All update resource names in '--update-id' must belong to the"
            " same location."
        )
      if inferred_wid and inferred_wid != u_wid:
        raise ValueError(
            "All update resource names in '--update-id' must belong to the"
            " same workload."
        )
      inferred_org, inferred_loc, inferred_wid = u_org, u_loc, u_wid

  if inferred_org and inferred_loc and inferred_wid:
    clean_org = normalize_org_id(organization) if organization else inferred_org
    if clean_org != inferred_org:
      raise ValueError(
          f"Organization ID mismatch: '--organization={clean_org}' does not"
          f" match '{inferred_org}' in '--update-id'."
      )
    clean_loc = validate_location(location) if location else inferred_loc
    if clean_loc != inferred_loc:
      raise ValueError(
          f"Location mismatch: '--location={clean_loc}' does not match"
          f" '{inferred_loc}' in '--update-id'."
      )
    clean_w_id = inferred_wid
    workload_name = f"organizations/{clean_org}/locations/{clean_loc}/workloads/{clean_w_id}"
  else:
    workload_name, clean_org, clean_loc, clean_w_id = (
        resolve_workload_resource_name(
            workload_id_or_name=workload_id,
            organization=organization,
            location=location,
        )
    )

  if len(raw_tokens) == 1 and raw_tokens[0].upper() == "ALL":
    clean_uid_arg = "ALL"
    clean_uids = ["ALL"]
    update_names: list[str] | None = None
    single_update_name: str | None = None
  else:
    clean_uids = []
    update_names = []
    for tok in raw_tokens:
      if tok.upper() == "ALL":
        raise ValueError(
            "'ALL' cannot be combined with individual update IDs in"
            " '--update-id'."
        )
      u_match = _UPDATE_RESOURCE_NAME_RE.fullmatch(tok)
      if u_match:
        u_id = u_match.group(4)
      else:
        if not _WORKLOAD_ID_RE.fullmatch(tok):
          raise ValueError(
              f"Invalid '--update-id' value '{tok}'. Expected update ID,"
              " comma-separated update IDs, 'ALL', or full update resource"
              " name"
              " 'organizations/<ORG>/locations/<LOC>/workloads/<WID>/updates/<UID>'."
          )
        u_id = tok
      if u_id not in clean_uids:
        clean_uids.append(u_id)
        update_names.append(f"{workload_name}/updates/{u_id}")
    clean_uid_arg = ",".join(clean_uids)
    single_update_name = update_names[0] if len(update_names) == 1 else None

  updates_script_path = _get_sibling_script_path("manage_workload_updates.py")
  apply_update_cmd = (
      f"python3 {shlex.quote(updates_script_path)} \\\n"
      "  --action=apply \\\n"
      f"  --organization={shlex.quote(clean_org)} \\\n"
      f"  --location={shlex.quote(clean_loc)} \\\n"
      f"  --workload-id={shlex.quote(clean_w_id)} \\\n"
      f"  --update-id={shlex.quote(clean_uid_arg)} \\\n"
      "  --poll-timeout-seconds=180 \\\n"
      "  --poll-interval-seconds=3"
  )

  normalized_params: dict[str, Any] = {
      "workloadName": workload_name,
      "workloadId": clean_w_id,
      "organization": clean_org,
      "location": clean_loc,
      "updateId": clean_uid_arg,
      "updateIds": clean_uids,
  }
  if single_update_name is not None:
    normalized_params["updateName"] = single_update_name
  if update_names is not None:
    normalized_params["updateNames"] = update_names

  return {
      "valid": True,
      "operation": "apply-update",
      "normalizedParams": normalized_params,
      "warnings": [],
      "applyUpdateCommand": apply_update_cmd,
      "consoleUrl": (
          "https://console.cloud.google.com/compliance/assuredworkloads"
          f"?organizationId={clean_org}"
      ),
  }


def build_arg_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(
      description=(
          "Validate Assured Workloads V1 parameters for create, list,"
          " describe (get), update, list-updates, apply-update, and delete"
          " operations."
      )
  )
  parser.add_argument(
      "--operation",
      default="create",
      choices=[
          "create",
          "list",
          "describe",
          "get",
          "update",
          "list-updates",
          "apply-update",
          "delete",
      ],
      help=(
          "Workload operation to validate: create, list, describe (alias:"
          " get), update, list-updates, apply-update, or delete."
      ),
  )
  parser.add_argument(
      "--organization",
      default=None,
      help="Numeric Google Cloud Organization ID (e.g., 123456789012).",
  )
  parser.add_argument(
      "--location",
      default=None,
      help="Regional or multi-regional location (e.g., us-central1, us, eu).",
  )
  parser.add_argument(
      "--workload-id",
      default=None,
      help=(
          "Workload ID or full resource name"
          " (organizations/<ORG>/locations/<LOC>/workloads/<ID>) for"
          " describe/get/update/list-updates/apply-update/delete."
      ),
  )
  parser.add_argument(
      "--update-id",
      default=None,
      help=(
          "Update ID or full update resource name"
          " (organizations/<ORG>/locations/<LOC>/workloads/<WID>/updates/<UID>)"
          " for --operation=apply-update."
      ),
  )
  parser.add_argument(
      "--enable-compliance-updates",
      action="store_true",
      help=(
          "Include --enable-compliance-updates in listUpdatesCommand for"
          " --operation=list-updates."
      ),
  )
  parser.add_argument(
      "--etag",
      default=None,
      help=(
          "Optional workload etag acquired by reading the Assured Workloads"
          " environment (used with --operation=update or --operation=delete)."
      ),
  )
  parser.add_argument(
      "--violation-notifications-enabled",
      default=None,
      help=(
          "Notification setting ('true' or 'false') for --operation=update"
          " (V1)."
      ),
  )
  parser.add_argument(
      "--display-name",
      default=None,
      help="Workload display name (4-30 chars, alphanumeric, spaces, hyphens).",
  )
  parser.add_argument(
      "--compliance-regime",
      default=None,
      help="Assured Workloads V1 compliance regime enum (e.g., FEDRAMP_HIGH).",
  )
  parser.add_argument(
      "--billing-account",
      default=None,
      help="Optional billing account in format billingAccounts/<ID>.",
  )
  parser.add_argument(
      "--provisioned-resources-parent",
      default=None,
      help="Optional parent folder in format folders/<FOLDER_ID>.",
  )
  parser.add_argument(
      "--restriction-type",
      default="ALLOW_COMPLIANT_RESOURCES",
      help=(
          "Phase 2 RestrictAllowedResources restriction type"
          " (ALLOW_COMPLIANT_RESOURCES, APPEND_COMPLIANT_RESOURCES, or"
          " ALLOW_ALL_GCP_RESOURCES)."
      ),
  )
  parser.add_argument(
      "--enable-sovereign-controls",
      action="store_true",
      help="Enable sovereign controls (KAJ / Access Transparency) if supported.",
  )
  parser.add_argument(
      "--partner",
      default=None,
      help="Partner enum when using ASSURED_WORKLOADS_FOR_PARTNERS.",
  )
  parser.add_argument(
      "--partner-permissions",
      default=None,
      help="Partner permissions map, e.g., data-logs-viewer=true.",
  )
  parser.add_argument(
      "--partner-services-billing-account",
      default=None,
      help=(
          "Billing account for Sovereign Controls by Partners workloads"
          " (required for SIA/PSN/CNTXT) in format billingAccounts/<ID>."
      ),
  )
  parser.add_argument(
      "--resource-settings",
      default=None,
      help=(
          "Comma-separated custom resource settings: consumer-project-id,"
          " consumer-project-name, encryption-keys-project-id,"
          " encryption-keys-project-name, keyring-id."
      ),
  )
  parser.add_argument(
      "--next-rotation-time",
      default=None,
      help=(
          "KMS key next rotation timestamp in RFC 3339 / ISO-8601 format (e.g.,"
          " 2026-12-30T10:15:30.00Z). Requires --rotation-period."
      ),
  )
  parser.add_argument(
      "--rotation-period",
      default=None,
      help=(
          "KMS key rotation period in seconds (e.g., 172800s). Requires"
          " --next-rotation-time."
      ),
  )
  parser.add_argument(
      "--labels",
      default=None,
      help="Comma-separated KEY=VALUE labels (e.g., env=prod,team=sec).",
  )
  parser.add_argument(
      "--external-identifier",
      default=None,
      help="Optional external identifier (1-63 alphanumeric/hyphen/underscore).",
  )
  parser.add_argument(
      "--limit",
      type=int,
      default=None,
      help="Optional maximum number of workloads to return for --operation=list.",
  )
  parser.add_argument(
      "--page-size",
      type=int,
      default=None,
      help="Optional page size for --operation=list.",
  )
  parser.add_argument(
      "--filter",
      dest="filter_expr",
      default=None,
      help="Optional gcloud filter expression for --operation=list.",
  )
  return parser


def main(argv: list[str] | None = None) -> int:
  parser = build_arg_parser()
  args = parser.parse_args(argv)
  try:
    if args.operation == "create":
      result = validate_create_params(
          organization=args.organization,
          location=args.location,
          display_name=args.display_name,
          compliance_regime=args.compliance_regime,
          billing_account=args.billing_account,
          provisioned_resources_parent=args.provisioned_resources_parent,
          restriction_type=args.restriction_type,
          enable_sovereign_controls=args.enable_sovereign_controls,
          partner=args.partner,
          partner_permissions=args.partner_permissions,
          partner_services_billing_account=args.partner_services_billing_account,
          resource_settings=args.resource_settings,
          next_rotation_time=args.next_rotation_time,
          rotation_period=args.rotation_period,
          labels=args.labels,
          external_identifier=args.external_identifier,
      )
    elif args.operation == "list":
      result = validate_list_params(
          organization=args.organization,
          location=args.location,
          limit=args.limit,
          page_size=args.page_size,
          filter_expr=args.filter_expr,
      )
    elif args.operation in ("describe", "get"):
      result = validate_describe_params(
          workload_id=args.workload_id,
          organization=args.organization,
          location=args.location,
      )
    elif args.operation == "update":
      result = validate_update_params(
          workload_id=args.workload_id,
          organization=args.organization,
          location=args.location,
          display_name=args.display_name,
          labels=args.labels,
          violation_notifications_enabled=args.violation_notifications_enabled,
          etag=args.etag,
      )
    elif args.operation == "list-updates":
      result = validate_list_updates_params(
          workload_id=args.workload_id,
          organization=args.organization,
          location=args.location,
          enable_compliance_updates=args.enable_compliance_updates,
      )
    elif args.operation == "apply-update":
      result = validate_apply_update_params(
          workload_id=args.workload_id,
          update_id=args.update_id,
          organization=args.organization,
          location=args.location,
      )
    elif args.operation == "delete":
      result = validate_delete_params(
          workload_id=args.workload_id,
          organization=args.organization,
          location=args.location,
          etag=args.etag,
      )
    else:
      raise ValueError(f"Unsupported operation '{args.operation}'.")

    print(json.dumps(result, indent=2))
    return 0
  except ValueError as err:
    sys.stderr.write(f"VALIDATION_ERROR: {err}\n")
    return 1


if __name__ == "__main__":
  sys.exit(main())
