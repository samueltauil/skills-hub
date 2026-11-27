#!/usr/bin/env python3
r"""Common error handler and LRO failure diagnostics for Assured Workloads V1.

Parses CLI / API error messages or inspects the latest failed Long-Running
Operation (LRO) in an organization and location (`operations.list` /
`operations.get`) to map public `google.rpc.ErrorInfo.reason` codes (`ERROR_CODE_*`)
to deterministic root causes and remediation steps across Create, List/Describe,
Update, and Delete workflows.

Usage examples:
  # Diagnose a CLI or API error message directly:
  python3 scripts/diagnose_error.py \
    --error-message="FAILED_PRECONDITION: ... ERROR_CODE_WORKLOAD_NOT_EMPTY"

  # Inspect the latest failed LRO when `gcloud assured workloads create` prints
  # "ERROR: (gcloud.assured.workloads.create) Folder creation was unsuccessful. Please try again.":
  python3 scripts/diagnose_error.py \
    --fetch-latest-lro \
    --organization=123456789012 \
    --location=us-central1
"""

import argparse
import json
import re
import sys
from typing import Any

USER_AGENT = "agent-skills/1.0 (skill:assured-workloads-basics)"
_ORG_ID_RE = re.compile(r"^\d+$")
_ERROR_CODE_RE = re.compile(r"\b(ERROR_CODE_[A-Z0-9_]+)\b")

_AXT_ERROR_ENTRY: dict[str, Any] = {
    "workflow": "create",
    "canonicalStatus": "FAILED_PRECONDITION",
    "retryable": False,
    "rootCause": (
        "Access Transparency is not enabled (or was disabled) on the"
        " Organization, which is required for this compliance regime or"
        " '--enable-sovereign-controls'."
    ),
    "remediation": (
        "Enable Access Transparency for the Google Cloud Organization in"
        " the Cloud Console (or contact Google Cloud Support if it was"
        " previously disabled) before creating the workload."
    ),
}

ERROR_CATALOG: dict[str, dict[str, Any]] = {
    "ERROR_CODE_FOLDER_CREATION_PRECONDITION_FAILED": {
        "workflow": "create",
        "canonicalStatus": "FAILED_PRECONDITION",
        "retryable": False,
        "rootCause": (
            "The target parent ('organizations/<ORG_ID>' or"
            " 'folders/<PARENT_FOLDER_ID>') reached the Cloud Resource Manager"
            " 300 direct child-folder quota or the 10-level folder nesting"
            " depth limit."
        ),
        "remediation": (
            "Pass '--provisioned-resources-parent=folders/<FOLDER_ID>' pointing"
            " to an existing non-workload parent folder with available"
            " child-folder capacity."
        ),
    },
    "ERROR_CODE_FOLDER_NAME_UNIQUENESS": {
        "workflow": "create",
        "canonicalStatus": "FAILED_PRECONDITION",
        "retryable": False,
        "rootCause": (
            "A sibling folder with the same '--display-name' already exists"
            " directly under the target parent."
        ),
        "remediation": (
            "Choose a unique '--display-name' or specify a different"
            " '--provisioned-resources-parent=folders/<FOLDER_ID>'."
        ),
    },
    "ERROR_CODE_INVALID_PROVISIONED_RESOURCES_PARENT": {
        "workflow": "create",
        "canonicalStatus": "INVALID_ARGUMENT",
        "retryable": False,
        "rootCause": (
            "The specified '--provisioned-resources-parent' folder is itself"
            " already an Assured Workloads folder (Assured Workloads"
            " environments cannot be nested inside another Assured Workloads"
            " folder)."
        ),
        "remediation": (
            "Select a standard non-workload folder for"
            " '--provisioned-resources-parent' or omit the flag to provision"
            " under the organization root."
        ),
    },
    "ERROR_CODE_PROJECT_ID_ALREADY_IN_USE": {
        "workflow": "create",
        "canonicalStatus": "INVALID_ARGUMENT",
        "retryable": False,
        "rootCause": (
            "The custom 'consumer-project-id' or 'encryption-keys-project-id'"
            " specified in '--resource-settings' is already in use globally."
        ),
        "remediation": (
            "Choose a globally unique project ID in '--resource-settings'."
        ),
    },
    "ERROR_CODE_PROJECT_DISPLAY_NAME_EXCEEDS_LIMIT": {
        "workflow": "create",
        "canonicalStatus": "FAILED_PRECONDITION",
        "retryable": False,
        "rootCause": (
            "The custom project display name ('consumer-project-name' or"
            " 'encryption-keys-project-name') exceeds 30 characters."
        ),
        "remediation": (
            "Shorten custom project display names in '--resource-settings' to"
            " 30 characters or fewer."
        ),
    },
    "ERROR_CODE_WORKLOAD_NOT_EMPTY": {
        "workflow": "delete",
        "canonicalStatus": "FAILED_PRECONDITION",
        "retryable": True,
        "rootCause": (
            "Assured Workloads workload deletion requires all provisioned"
            " Cloud Resource Manager projects ('ENCRYPTION_KEYS_PROJECT',"
            " 'CONSUMER_PROJECT') and the workload folder ('CONSUMER_FOLDER')"
            " to be deleted first, or folder deletion status"
            " ('DELETE_REQUESTED') is still propagating (15-60 seconds)."
        ),
        "remediation": (
            "Case A (Underlying folder/projects still active): Obtain explicit"
            " user confirmation, delete any projects inside the folder first"
            " ('gcloud projects delete <PROJECT_ID> --quiet'), then delete the"
            " workload folder ('gcloud resource-manager folders delete"
            " <FOLDER_ID>'). Case B (Folder was deleted within the last 60"
            " seconds): Wait 15-20 seconds for Cloud Resource Manager folder"
            " deletion status to propagate and retry 'gcloud assured workloads"
            " delete' (up to 3 times over 60s, omitting '--etag')."
        ),
    },
    "ERROR_CODE_COMPLIANCE_UPDATE_NOT_ENABLED": {
        "workflow": "update",
        "canonicalStatus": "FAILED_PRECONDITION",
        "retryable": False,
        "rootCause": (
            "Compliance configuration updates are not yet enabled on this"
            " older Assured Workloads folder."
        ),
        "remediation": (
            "Re-run 'python3 scripts/manage_workload_updates.py --action=list"
            " --enable-compliance-updates' (or '--action=enable'). Ensure the"
            " caller holds 'roles/resourcemanager.folderIamAdmin' on the"
            " folder."
        ),
    },
    "ERROR_CODE_WORKLOAD_UPDATE_NOT_APPLICABLE": {
        "workflow": "update",
        "canonicalStatus": "FAILED_PRECONDITION",
        "retryable": False,
        "rootCause": (
            "The organization policy on the workload folder was manually"
            " modified after the workload update became available."
        ),
        "remediation": (
            "Compare the folder's current organization policy with"
            " 'details.orgPolicyUpdate.appliedPolicy', restore the previous"
            " organization policy setting on the folder (or wait for the next"
            " periodic update evaluation), and re-run '--action=list'."
        ),
    },
    "ERROR_CODE_PERMISSION_DENIED": {
        "workflow": "all",
        "canonicalStatus": "PERMISSION_DENIED",
        "retryable": False,
        "rootCause": (
            "The caller or the Assured Workloads Service Agent is missing"
            " required IAM permissions."
        ),
        "remediation": (
            "Check 'metadata.missing_permissions' in the error output. Verify"
            " the caller holds 'roles/assuredworkloads.admin' on"
            " 'organizations/<ORG_ID>' (plus 'roles/billing.user' on the"
            " billing account when creating workloads) and that"
            " 'service-<ORG_NUMBER>@gcp-sa-assuredworkloads.iam.gserviceaccount.com'"
            " holds 'roles/assuredworkloads.serviceAgent'."
        ),
    },
    "ERROR_CODE_BILLING_ACCOUNT_INVALID": {
        "workflow": "create",
        "canonicalStatus": "INVALID_ARGUMENT",
        "retryable": False,
        "rootCause": (
            "The specified '--billing-account' (or"
            " '--partner-services-billing-account') is invalid, closed, or the"
            " caller lacks permissions to associate it."
        ),
        "remediation": (
            "Run 'gcloud billing accounts list --filter=\"open=true\"' to"
            " select an active billing account and verify the caller holds"
            " 'roles/billing.user' (and 'billing.resourceAssociations.create'"
            " for partner billing accounts)."
        ),
    },
    "ERROR_CODE_BILLING_QUOTA_EXCEEDED": {
        "workflow": "create",
        "canonicalStatus": "RESOURCE_EXHAUSTED",
        "retryable": False,
        "rootCause": (
            "The billing account has reached its maximum linked project quota."
        ),
        "remediation": (
            "Select a different open billing account or request a billing"
            " account project quota increase."
        ),
    },
    "ERROR_CODE_ACCESS_TRANSPARENCY_NOT_ENABLED": _AXT_ERROR_ENTRY,
    "ERROR_CODE_ACCESS_TRANSPARENCY_DISABLED": _AXT_ERROR_ENTRY,
}


def _create_discovery_service(location: str) -> Any:
  """Creates a regional Assured Workloads v1 Discovery service with telemetry."""
  try:
    import google.auth  # pylint: disable=g-import-not-at-top
    from google.api_core.client_options import ClientOptions  # pylint: disable=g-import-not-at-top
    from googleapiclient import discovery  # pylint: disable=g-import-not-at-top
    import googleapiclient.http  # pylint: disable=g-import-not-at-top
  except ImportError as exc:
    raise RuntimeError(
        "Missing required Python packages 'google-api-python-client' and"
        " 'google-auth'. Install via: pip install"
        ' "google-api-python-client>=2.0,<3" "google-auth>=2.0,<3"'
    ) from exc

  credentials, _ = google.auth.default()
  endpoint = f"https://{location}-assuredworkloads.googleapis.com"
  service = discovery.build(
      "assuredworkloads",
      "v1",
      credentials=credentials,
      client_options=ClientOptions(api_endpoint=endpoint),
  )
  if hasattr(service, "_http") and hasattr(
      googleapiclient.http, "set_user_agent"
  ):
    googleapiclient.http.set_user_agent(service._http, USER_AGENT)
  return service


def fetch_latest_failed_lro(
    organization: str,
    location: str,
    limit: int = 5,
    service: Any = None,
) -> dict[str, Any] | None:
  """Fetches the most recent failed LRO in organizations/<ORG>/locations/<LOC>."""
  clean_org = organization.strip()
  if clean_org.startswith("organizations/"):
    clean_org = clean_org[len("organizations/") :].strip()
  if not _ORG_ID_RE.fullmatch(clean_org):
    raise ValueError(
        f"Invalid organization ID '{organization}'. Expected numeric ID."
    )
  clean_loc = location.strip().lower()
  if not clean_loc or clean_loc == "global":
    raise ValueError(
        f"Invalid location '{location}'. Assured Workloads V1 requires a"
        " regional or multi-regional location."
    )

  if service is None:
    service = _create_discovery_service(clean_loc)

  parent = f"organizations/{clean_org}/locations/{clean_loc}"
  ops_resource = service.organizations().locations().operations()
  response = ops_resource.list(name=parent, pageSize=limit).execute() or {}
  operations = response.get("operations", [])
  for op in operations:
    if "error" in op:
      return op
  return None


def diagnose_error(
    error_message: str | None = None,
    fetch_latest_lro: bool = False,
    organization: str | None = None,
    location: str | None = None,
    service: Any = None,
) -> dict[str, Any]:
  """Diagnoses an Assured Workloads CLI/API error or failed LRO."""
  if not error_message and not fetch_latest_lro:
    raise ValueError(
        "Provide '--error-message' and/or '--fetch-latest-lro' (with"
        " '--organization' and '--location')."
    )

  failed_lro: dict[str, Any] | None = None
  combined_text = error_message or ""

  if fetch_latest_lro:
    if not organization or not location:
      raise ValueError(
          "'--organization' and '--location' are required when"
          " '--fetch-latest-lro' is set."
      )
    failed_lro = fetch_latest_failed_lro(
        organization=organization,
        location=location,
        service=service,
    )
    if failed_lro:
      combined_text = f"{combined_text}\n{json.dumps(failed_lro)}"

  matched_codes: list[str] = []
  for match in _ERROR_CODE_RE.finditer(combined_text):
    code = match.group(1)
    if code not in matched_codes:
      matched_codes.append(code)

  if (
      not matched_codes
      and "Folder creation was unsuccessful. Please try again." in combined_text
      and not fetch_latest_lro
  ):
    return {
        "status": "NEEDS_LRO_INSPECTION",
        "retryable": False,
        "rootCause": (
            "gcloud assured workloads create returned a generic folder creation"
            " error. The underlying reason is recorded on the Long-Running"
            " Operation (LRO)."
        ),
        "remediation": (
            "Do not blindly retry 'gcloud assured workloads create'. Re-run"
            " 'python3 scripts/diagnose_error.py --fetch-latest-lro"
            " --organization=<ORG_ID> --location=<LOCATION>' (or run 'gcloud"
            " assured operations list --organization=<ORG_ID>"
            " --location=<LOCATION> --limit=5 --format=json') to inspect the"
            " LRO error code."
        ),
    }

  diagnoses: list[dict[str, Any]] = []
  for code in matched_codes:
    if code in ERROR_CATALOG:
      entry = dict(ERROR_CATALOG[code])
      entry["errorCode"] = code
      diagnoses.append(entry)
    else:
      diagnoses.append({
          "errorCode": code,
          "workflow": "unknown",
          "canonicalStatus": "UNKNOWN",
          "retryable": False,
          "rootCause": f"Assured Workloads returned error code '{code}'.",
          "remediation": (
              "Inspect the full error details and verify input parameters, IAM"
              " roles, and resource preconditions before retrying."
          ),
      })

  if not diagnoses:
    return {
        "status": "UNRECOGNIZED_ERROR",
        "retryable": False,
        "matchedErrorCodes": [],
        "failedOperation": failed_lro.get("name") if failed_lro else None,
        "rootCause": (
            "No specific Assured Workloads ERROR_CODE_* token was found in the"
            " error output."
        ),
        "remediation": (
            "Do not blindly retry deterministic 400/403/404 errors. Verify"
            " parameters with 'scripts/validate_params.py' and check IAM roles"
            " in Step 0."
        ),
    }

  primary = diagnoses[0]
  result: dict[str, Any] = {
      "status": "DIAGNOSED",
      "primaryErrorCode": primary["errorCode"],
      "workflow": primary["workflow"],
      "canonicalStatus": primary["canonicalStatus"],
      "retryable": primary["retryable"],
      "rootCause": primary["rootCause"],
      "remediation": primary["remediation"],
      "matchedErrorCodes": matched_codes,
      "diagnoses": diagnoses,
  }
  if failed_lro:
    result["failedOperationName"] = failed_lro.get("name")
    result["failedOperationError"] = failed_lro.get("error")
  return result


def build_arg_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(
      description=(
          "Diagnose Assured Workloads V1 CLI/API errors and failed"
          " Long-Running Operations."
      )
  )
  parser.add_argument(
      "--error-message",
      default=None,
      help="Raw error string or JSON output from gcloud or Python script.",
  )
  parser.add_argument(
      "--fetch-latest-lro",
      action="store_true",
      help=(
          "Query the Assured Workloads operations.list API to inspect the most"
          " recent failed LRO in --organization and --location."
      ),
  )
  parser.add_argument(
      "--organization",
      default=None,
      help="Numeric Organization ID (required when --fetch-latest-lro is set).",
  )
  parser.add_argument(
      "--location",
      default=None,
      help=(
          "Regional or multi-regional location (required when"
          " --fetch-latest-lro is set)."
      ),
  )
  return parser


def main(argv: list[str] | None = None) -> int:
  parser = build_arg_parser()
  args = parser.parse_args(argv)
  try:
    result = diagnose_error(
        error_message=args.error_message,
        fetch_latest_lro=args.fetch_latest_lro,
        organization=args.organization,
        location=args.location,
    )
    print(json.dumps(result, indent=2))
    return 0
  except (ValueError, RuntimeError) as err:
    sys.stderr.write(f"DIAGNOSE_ERROR_FAILURE: {err}\n")
    return 1


if __name__ == "__main__":
  sys.exit(main())
