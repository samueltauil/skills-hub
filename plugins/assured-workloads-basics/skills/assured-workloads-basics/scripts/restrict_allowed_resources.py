#!/usr/bin/env python3
r"""Phase 2 helper for Assured Workloads creation: RestrictAllowedResources.

Checks a workload's `compliant_but_disallowed_services` via `GetWorkload` and
invokes `AssuredWorkloadsServiceClient.restrict_allowed_resources()` to enable
compliant services on the workload folder's `gcp.restrictServiceUsage`
organization policy.

Why Python Client Library?
  `gcloud assured workloads` does not expose a CLI subcommand for the
  `RestrictAllowedResources` RPC. Per the hybrid CLI + Client Library pattern,
  this script uses `google-cloud-assured-workloads` with regional endpoint
  routing (`{location}-assuredworkloads.googleapis.com`) and user-agent
  telemetry (`agent-skills/1.0 (skill:assured-workloads-basics)`).

Usage example:
  python3 scripts/restrict_allowed_resources.py \
    --organization=123456789012 \
    --location=us-central1 \
    --workload-id=9876543210 \
    --restriction-type=ALLOW_COMPLIANT_RESOURCES
"""

import argparse
import json
import re
import sys
import time
from typing import Any

USER_AGENT = "agent-skills/1.0 (skill:assured-workloads-basics)"

RESTRICTION_TYPE_ENUM_VALUES: dict[str, int] = {
    "ALLOW_ALL_GCP_RESOURCES": 1,
    "ALLOW_COMPLIANT_RESOURCES": 2,
    "APPEND_COMPLIANT_RESOURCES": 3,
}

REGIMES_WITHOUT_BQ_ONBOARDING_DELAY: frozenset[str] = frozenset({
    "FEDRAMP_MODERATE",
    "DATA_BOUNDARY_FOR_FEDRAMP_MODERATE",
})

# Maps ComplianceRegime enum IDs to canonical names for client library versions
# that return raw integer IDs for newer regimes (e.g. 32, 44).
COMPLIANCE_REGIME_ID_TO_NAME: dict[int, str] = {
    0: "COMPLIANCE_REGIME_UNSPECIFIED",
    1: "IL4",
    2: "CJIS",
    3: "FEDRAMP_HIGH",
    4: "FEDRAMP_MODERATE",
    5: "US_REGIONAL_ACCESS",
    6: "HIPAA",
    7: "HITRUST",
    8: "EU_REGIONS_AND_SUPPORT",
    9: "CA_REGIONS_AND_SUPPORT",
    10: "ITAR",
    11: "AU_REGIONS_AND_US_SUPPORT",
    12: "ASSURED_WORKLOADS_FOR_PARTNERS",
    13: "ISR_REGIONS_AND_SUPPORT",
    14: "CA_PROTECTED_B",
    15: "IL5",
    16: "IL2",
    17: "JP_REGIONS_AND_SUPPORT",
    20: "KSA_REGIONS_AND_SUPPORT_WITH_SOVEREIGNTY_CONTROLS",
    21: "REGIONAL_CONTROLS",
    22: "HEALTHCARE_AND_LIFE_SCIENCES_CONTROLS",
    23: "HEALTHCARE_AND_LIFE_SCIENCES_CONTROLS_US_SUPPORT",
    24: "IRS_1075",
    25: "CANADA_CONTROLLED_GOODS",
    26: "AUSTRALIA_DATA_BOUNDARY_AND_SUPPORT",
    27: "CANADA_DATA_BOUNDARY_AND_SUPPORT",
    28: "DATA_BOUNDARY_FOR_CANADA_CONTROLLED_GOODS",
    29: "DATA_BOUNDARY_FOR_CANADA_PROTECTED_B",
    30: "DATA_BOUNDARY_FOR_CJIS",
    31: "DATA_BOUNDARY_FOR_FEDRAMP_HIGH",
    32: "DATA_BOUNDARY_FOR_FEDRAMP_MODERATE",
    33: "DATA_BOUNDARY_FOR_IL2",
    34: "DATA_BOUNDARY_FOR_IL4",
    35: "DATA_BOUNDARY_FOR_IL5",
    36: "DATA_BOUNDARY_FOR_IRS_PUBLICATION_1075",
    37: "DATA_BOUNDARY_FOR_ITAR",
    38: "EU_DATA_BOUNDARY_AND_SUPPORT",
    39: "ISRAEL_DATA_BOUNDARY_AND_SUPPORT",
    40: "US_DATA_BOUNDARY_AND_SUPPORT",
    41: "US_DATA_BOUNDARY_FOR_HEALTHCARE_AND_LIFE_SCIENCES",
    42: "US_DATA_BOUNDARY_FOR_HEALTHCARE_AND_LIFE_SCIENCES_WITH_SUPPORT",
    43: "KSA_DATA_BOUNDARY_WITH_ACCESS_JUSTIFICATIONS",
    44: "REGIONAL_DATA_BOUNDARY",
    45: "JAPAN_DATA_BOUNDARY",
    46: "SWITZERLAND_DATA_BOUNDARY_WITH_ACCESS_JUSTIFICATIONS",
}


def _extract_regime_name(workload: Any) -> str:
  """Extracts the string name of workload.compliance_regime.

  Handles resolved enum objects, string names, and raw integer enum
  values returned when the installed google-cloud-assured-workloads library's
  enum table predates newer backend regimes.
  """
  raw_regime = getattr(workload, "compliance_regime", None)
  if raw_regime is None:
    return ""
  regime_name = getattr(raw_regime, "name", None)
  if isinstance(regime_name, str) and regime_name:
    return regime_name
  if isinstance(raw_regime, int):
    return COMPLIANCE_REGIME_ID_TO_NAME.get(raw_regime, str(raw_regime))
  if isinstance(raw_regime, str):
    clean = raw_regime.strip()
    if clean.isdigit():
      return COMPLIANCE_REGIME_ID_TO_NAME.get(int(clean), clean)
    return clean
  raw_str = str(raw_regime).strip()
  if raw_str.isdigit():
    return COMPLIANCE_REGIME_ID_TO_NAME.get(int(raw_str), raw_str)
  return raw_str

_WORKLOAD_NAME_RE = re.compile(
    r"^organizations/(\d+)/locations/([a-z0-9-]+)/workloads/([a-zA-Z0-9_-]+)$"
)
_ORG_ID_RE = re.compile(r"^\d+$")
_WORKLOAD_ID_RE = re.compile(r"^[a-zA-Z0-9_-]+$")


def build_workload_resource_name(
    organization: str | None,
    location: str | None,
    workload_id_or_name: str,
) -> tuple[str, str, str, str]:
  """Resolves and validates (workload_name, org_id, location, workload_id)."""
  candidate = workload_id_or_name.strip()
  match = _WORKLOAD_NAME_RE.fullmatch(candidate)
  if match:
    org_id, loc, w_id = match.group(1), match.group(2), match.group(3)
    if loc == "global":
      raise ValueError(
          "Invalid location 'global' in workload resource name. Assured"
          " Workloads V1 requires a regional or multi-regional location."
      )
    return candidate, org_id, loc, w_id

  if not organization or not organization.strip():
    raise ValueError(
        "Missing '--organization' when '--workload-id' is not a full resource"
        " path."
    )
  if not location or not location.strip():
    raise ValueError(
        "Missing '--location' when '--workload-id' is not a full resource path."
    )

  clean_org = organization.strip()
  if clean_org.startswith("organizations/"):
    clean_org = clean_org[len("organizations/") :].strip()
  if not _ORG_ID_RE.fullmatch(clean_org):
    raise ValueError(
        f"Invalid organization ID '{organization}'. Expected numeric ID."
    )

  clean_loc = location.strip().lower()
  if clean_loc == "global":
    raise ValueError(
        "Invalid location 'global'. Assured Workloads V1 requires a regional or"
        " multi-regional location (e.g., 'us-central1', 'us', 'eu')."
    )

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


def validate_restriction_type(restriction_type: str) -> tuple[str, int]:
  """Validates restriction_type string and returns (normalized_name, enum_int)."""
  clean = restriction_type.strip().upper().replace("-", "_")
  if clean not in RESTRICTION_TYPE_ENUM_VALUES:
    raise ValueError(
        f"Invalid restriction type '{restriction_type}'. Valid values:"
        f" {sorted(RESTRICTION_TYPE_ENUM_VALUES.keys())}"
    )
  return clean, RESTRICTION_TYPE_ENUM_VALUES[clean]


def create_default_client(location: str) -> Any:
  """Instantiates AssuredWorkloadsServiceClient with regional endpoint & UA."""
  try:
    from google.api_core.client_options import ClientOptions  # pylint: disable=g-import-not-at-top
    from google.api_core.gapic_v1.client_info import ClientInfo  # pylint: disable=g-import-not-at-top
    from google.cloud import assuredworkloads_v1  # pylint: disable=g-import-not-at-top
  except ImportError as err:
    raise RuntimeError(
        "Missing 'google-cloud-assured-workloads' package. Install prerequisites"
        ' first: pip install "google-cloud-assured-workloads>=1.0,<2"'
        ' "google-api-python-client>=2.0,<3" "google-auth>=2.0,<3"'
    ) from err

  endpoint = f"{location}-assuredworkloads.googleapis.com"
  client_options = ClientOptions(api_endpoint=endpoint)
  client_info = ClientInfo(user_agent=USER_AGENT)
  return assuredworkloads_v1.AssuredWorkloadsServiceClient(
      client_options=client_options,
      client_info=client_info,
      transport="rest",
  )


def execute_restrict_allowed_resources(
    workload_id: str,
    organization: str | None = None,
    location: str | None = None,
    restriction_type: str = "ALLOW_COMPLIANT_RESOURCES",
    poll_timeout_seconds: int = 0,
    poll_interval_seconds: int = 15,
    force: bool = False,
    dry_run: bool = False,
    client: Any = None,
) -> dict[str, Any]:
  """Checks compliant_but_disallowed_services and restricts allowed resources."""
  workload_name, org_id, loc, w_id = build_workload_resource_name(
      organization, location, workload_id
  )
  clean_restriction, restriction_enum_int = validate_restriction_type(
      restriction_type
  )
  regional_endpoint = f"{loc}-assuredworkloads.googleapis.com"

  if dry_run:
    return {
        "status": "DRY_RUN",
        "workloadName": workload_name,
        "organization": org_id,
        "location": loc,
        "workloadId": w_id,
        "regionalEndpoint": regional_endpoint,
        "userAgent": USER_AGENT,
        "request": {
            "name": workload_name,
            "restrictionType": clean_restriction,
            "restrictionTypeEnum": restriction_enum_int,
        },
    }

  active_client = client if client is not None else create_default_client(loc)

  deadline = time.monotonic() + max(0, poll_timeout_seconds)
  compliant_but_disallowed: list[str] = []
  regime_name = ""

  while True:
    workload = active_client.get_workload(request={"name": workload_name})
    raw_services = getattr(workload, "compliant_but_disallowed_services", [])
    compliant_but_disallowed = list(raw_services) if raw_services else []
    regime_name = _extract_regime_name(workload)

    if (
        not compliant_but_disallowed
        and regime_name in REGIMES_WITHOUT_BQ_ONBOARDING_DELAY
        and not force
    ):
      return {
          "status": "ALREADY_ALLOWLISTED_AT_CREATION",
          "workloadName": workload_name,
          "regionalEndpoint": regional_endpoint,
          "complianceRegime": regime_name,
          "compliantButDisallowedServices": [],
          "message": (
              f"Control package '{regime_name}' automatically enables all"
              " supported services (including BigQuery) when the folder is"
              " created. No additional service enablement step is required."
          ),
      }

    if compliant_but_disallowed or time.monotonic() >= deadline:
      break
    time.sleep(max(1, poll_interval_seconds))

  if not compliant_but_disallowed and not force:
    return {
        "status": "SKIPPED_NO_DISALLOWED_COMPLIANT_SERVICES",
        "workloadName": workload_name,
        "regionalEndpoint": regional_endpoint,
        "compliantButDisallowedServices": [],
        "message": (
            "No additional compliant services are currently listed in"
            " compliantButDisallowedServices. If this folder was just created,"
            " the background configuration process for BigQuery may still be in"
            " progress (typically 5-10 minutes). Pass"
            " --poll-timeout-seconds=300 to wait for it to finish, or re-run"
            " this command later."
        ),
    }

  active_client.restrict_allowed_resources(
      request={
          "name": workload_name,
          "restriction_type": restriction_enum_int,
      }
  )

  return {
      "status": "RESTRICTED_ALLOWED_RESOURCES",
      "workloadName": workload_name,
      "regionalEndpoint": regional_endpoint,
      "restrictionType": clean_restriction,
      "previouslyDisallowedCompliantServicesCount": len(
          compliant_but_disallowed
      ),
      "previouslyDisallowedCompliantServices": compliant_but_disallowed,
  }


def build_arg_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(
      description=(
          "Inspect workload.compliant_but_disallowed_services and invoke"
          " RestrictAllowedResources via google-cloud-assured-workloads."
      )
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
      required=True,
      help=(
          "Workload ID or full resource name"
          " (organizations/<ORG>/locations/<LOC>/workloads/<ID>)."
      ),
  )
  parser.add_argument(
      "--restriction-type",
      default="ALLOW_COMPLIANT_RESOURCES",
      help=(
          "RestrictionType enum: ALLOW_COMPLIANT_RESOURCES (default),"
          " APPEND_COMPLIANT_RESOURCES, or ALLOW_ALL_GCP_RESOURCES."
      ),
  )
  parser.add_argument(
      "--poll-timeout-seconds",
      type=int,
      default=0,
      help=(
          "Optional timeout in seconds to poll GetWorkload waiting for"
          " compliant_but_disallowed_services to populate (default: 0)."
      ),
  )
  parser.add_argument(
      "--poll-interval-seconds",
      type=int,
      default=10,
      help="Interval in seconds between GetWorkload polls (default: 10).",
  )
  parser.add_argument(
      "--force",
      action="store_true",
      help=(
          "Invoke RestrictAllowedResources even if"
          " compliant_but_disallowed_services is currently empty."
      ),
  )
  parser.add_argument(
      "--dry-run",
      action="store_true",
      help="Validate inputs and print the planned RPC request without calling API.",
  )
  return parser


def main(argv: list[str] | None = None) -> int:
  parser = build_arg_parser()
  args = parser.parse_args(argv)
  try:
    result = execute_restrict_allowed_resources(
        workload_id=args.workload_id,
        organization=args.organization,
        location=args.location,
        restriction_type=args.restriction_type,
        poll_timeout_seconds=args.poll_timeout_seconds,
        poll_interval_seconds=args.poll_interval_seconds,
        force=args.force,
        dry_run=args.dry_run,
    )
    print(json.dumps(result, indent=2))
    return 0
  except (ValueError, RuntimeError) as err:
    sys.stderr.write(f"ERROR: {err}\n")
    return 1
  except Exception as err:  # pylint: disable=broad-exception-caught
    sys.stderr.write(f"ERROR: {err}\n")
    return 1


if __name__ == "__main__":
  sys.exit(main())
