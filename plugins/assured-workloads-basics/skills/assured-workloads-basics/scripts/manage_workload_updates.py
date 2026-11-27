#!/usr/bin/env python3
r"""Helper for Assured Workloads V1 configuration updates (List & Apply Updates).

Uses the Google API Python Client Library (`google-api-python-client`) to:
  1. Enable workload compliance updates (`enableComplianceUpdates`) if needed.
  2. List available organization policy configuration updates (`updates.list`).
  3. Apply one, multiple, or all available workload updates (`updates.apply`)
     sequentially and poll each resulting Long-Running Operation
     (`operations.get`) until completion.

Why Python Client Library?
  `gcloud assured workloads update` only updates V1 workload metadata
  (`--display-name`, `--labels`, `--violation-notifications-enabled`) and does
  not expose CLI subcommands for V1 compliance posture updates
  (`enableComplianceUpdates`, `updates.list`, `updates.apply`). Per the official
  Google Cloud documentation and hybrid CLI + Client Library pattern, this
  script uses `google-api-python-client` with regional endpoint routing
  (`https://{location}-assuredworkloads.googleapis.com`) and user-agent
  telemetry (`agent-skills/1.0 (skill:assured-workloads-basics)`).

Usage examples:
  # List available configuration updates for a workload:
  python3 scripts/manage_workload_updates.py \
    --action=list \
    --organization=123456789012 \
    --location=us-central1 \
    --workload-id=00-701ea036-7152-4781-a867-9f5

  # Apply a specific configuration update by update ID:
  python3 scripts/manage_workload_updates.py \
    --action=apply \
    --organization=123456789012 \
    --location=us-central1 \
    --workload-id=00-701ea036-7152-4781-a867-9f5 \
    --update-id=5320de45-6c98-41af-b4a0-2ef930b124c3

  # Apply all available configuration updates sequentially:
  python3 scripts/manage_workload_updates.py \
    --action=apply \
    --organization=123456789012 \
    --location=us-central1 \
    --workload-id=00-701ea036-7152-4781-a867-9f5 \
    --update-id=ALL
"""

import argparse
import json
import re
import sys
import time
from typing import Any

USER_AGENT = "agent-skills/1.0 (skill:assured-workloads-basics)"

_WORKLOAD_NAME_RE = re.compile(
    r"^organizations/(\d+)/locations/([a-z0-9-]+)/workloads/([a-zA-Z0-9_-]+)$"
)
_UPDATE_NAME_RE = re.compile(
    r"^organizations/(\d+)/locations/([a-z0-9-]+)/workloads/([a-zA-Z0-9_-]+)/updates/([a-zA-Z0-9_-]+)$"
)
_ORG_ID_RE = re.compile(r"^\d+$")
_ID_TOKEN_RE = re.compile(r"^[a-zA-Z0-9_-]+$")


def resolve_workload_and_update_names(
    action: str,
    workload_id: str | None = None,
    organization: str | None = None,
    location: str | None = None,
    update_id: str | None = None,
) -> tuple[str, str, str, str, list[str] | None, list[str] | None]:
  """Resolves (workload_name, org_id, location, workload_id, update_names, update_ids)."""
  clean_action = action.strip().lower()
  if clean_action not in ("list", "enable", "apply"):
    raise ValueError(
        f"Invalid '--action' value '{action}'. Valid values: ['list', 'enable',"
        " 'apply']."
    )

  raw_tokens: list[str] = []
  if update_id and update_id.strip():
    raw_tokens = [t.strip() for t in update_id.split(",") if t.strip()]

  # First check if a single or multiple full update resource names were passed
  inferred_org: str | None = None
  inferred_loc: str | None = None
  inferred_wid: str | None = None
  for tok in raw_tokens:
    u_match = _UPDATE_NAME_RE.fullmatch(tok)
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
    if organization and organization.strip():
      norm_org = organization.strip()
      if norm_org.startswith("organizations/"):
        norm_org = norm_org[len("organizations/") :].strip()
      if norm_org != inferred_org:
        raise ValueError(
            f"Organization ID mismatch: '--organization={norm_org}' does not"
            f" match '{inferred_org}' in '--update-id'."
        )
    if location and location.strip():
      norm_loc = location.strip().lower()
      if norm_loc != inferred_loc:
        raise ValueError(
            f"Location mismatch: '--location={norm_loc}' does not match"
            f" '{inferred_loc}' in '--update-id'."
        )
    clean_org = inferred_org
    clean_loc = inferred_loc
    clean_wid = inferred_wid
    workload_name = (
        f"organizations/{clean_org}/locations/{clean_loc}/workloads/{clean_wid}"
    )
  else:
    if not workload_id or not workload_id.strip():
      raise ValueError(
          "Missing required '--workload-id' (or full resource name"
          " 'organizations/<ORG>/locations/<LOC>/workloads/<ID>')."
      )

    cand_workload = workload_id.strip()
    w_match = _WORKLOAD_NAME_RE.fullmatch(cand_workload)
    if w_match:
      clean_org, clean_loc, clean_wid = (
          w_match.group(1),
          w_match.group(2),
          w_match.group(3),
      )
      if clean_loc == "global":
        raise ValueError(
            "Invalid location 'global' in workload resource name. Assured"
            " Workloads V1 requires a regional or multi-regional location."
        )
      if organization and organization.strip():
        norm_org = organization.strip()
        if norm_org.startswith("organizations/"):
          norm_org = norm_org[len("organizations/") :].strip()
        if norm_org != clean_org:
          raise ValueError(
              f"Organization ID mismatch: '--organization={norm_org}' does not"
              f" match '{clean_org}' in '--workload-id'."
          )
      if location and location.strip():
        norm_loc = location.strip().lower()
        if norm_loc != clean_loc:
          raise ValueError(
              f"Location mismatch: '--location={norm_loc}' does not match"
              f" '{clean_loc}' in '--workload-id'."
          )
      workload_name = cand_workload
    else:
      if not organization or not organization.strip():
        raise ValueError(
            "Missing '--organization' when '--workload-id' is not a full"
            " resource path."
        )
      if not location or not location.strip():
        raise ValueError(
            "Missing '--location' when '--workload-id' is not a full resource"
            " path."
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
            "Invalid location 'global'. Assured Workloads V1 requires a"
            " regional or multi-regional location (e.g., 'us-central1', 'us',"
            " 'eu')."
        )
      if not _ID_TOKEN_RE.fullmatch(cand_workload):
        raise ValueError(
            f"Invalid workload ID '{workload_id}'. Expected workload ID or full"
            " resource name"
            " 'organizations/<ORG>/locations/<LOC>/workloads/<ID>'."
        )
      clean_wid = cand_workload
      workload_name = (
          f"organizations/{clean_org}/locations/{clean_loc}/workloads/{clean_wid}"
      )

  if clean_action == "apply":
    if not raw_tokens:
      raise ValueError(
          "Missing required '--update-id' when '--action=apply'. Pass a"
          " specific update ID, comma-separated update IDs, or"
          " '--update-id=ALL'."
      )
    if len(raw_tokens) == 1 and raw_tokens[0].upper() == "ALL":
      return workload_name, clean_org, clean_loc, clean_wid, None, ["ALL"]

    update_names: list[str] = []
    update_ids: list[str] = []
    for tok in raw_tokens:
      if tok.upper() == "ALL":
        raise ValueError(
            "'ALL' cannot be combined with individual update IDs in"
            " '--update-id'."
        )
      u_match = _UPDATE_NAME_RE.fullmatch(tok)
      if u_match:
        u_id = u_match.group(4)
        u_name = f"{workload_name}/updates/{u_id}"
      else:
        if not _ID_TOKEN_RE.fullmatch(tok):
          raise ValueError(
              f"Invalid '--update-id' value '{tok}'. Expected update ID,"
              " comma-separated update IDs, 'ALL', or full update resource"
              " name"
              " 'organizations/<ORG>/locations/<LOC>/workloads/<WID>/updates/<UID>'."
          )
        u_id = tok
        u_name = f"{workload_name}/updates/{u_id}"
      if u_id not in update_ids:
        update_ids.append(u_id)
        update_names.append(u_name)

    return (
        workload_name,
        clean_org,
        clean_loc,
        clean_wid,
        update_names,
        update_ids,
    )

  return workload_name, clean_org, clean_loc, clean_wid, None, None


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


def _fetch_all_updates(
    updates_resource: Any, workload_name: str, page_size: int
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, int]]:
  """Fetches all updates for a workload and computes state counts."""
  all_updates: list[dict[str, Any]] = []
  page_token: str | None = None
  while True:
    req_kwargs: dict[str, Any] = {
        "parent": workload_name,
        "pageSize": page_size,
    }
    if page_token:
      req_kwargs["pageToken"] = page_token
    response = updates_resource.list(**req_kwargs).execute() or {}
    batch = response.get("workloadUpdates", [])
    if batch:
      all_updates.extend(batch)
    page_token = response.get("nextPageToken")
    if not page_token:
      break

  available_updates = [
      u for u in all_updates if u.get("state") == "AVAILABLE"
  ]
  state_counts = {
      "AVAILABLE": len(available_updates),
      "APPLIED": sum(1 for u in all_updates if u.get("state") == "APPLIED"),
      "WITHDRAWN": sum(
          1 for u in all_updates if u.get("state") == "WITHDRAWN"
      ),
      "TOTAL": len(all_updates),
  }
  return all_updates, available_updates, state_counts


def _apply_single_update_and_poll(
    updates_resource: Any,
    operations_resource: Any,
    workload_name: str,
    update_name: str,
    update_id: str,
    poll_timeout_seconds: int,
    poll_interval_seconds: int,
) -> dict[str, Any]:
  """Applies a single update and polls its LRO until completion or timeout."""
  operation = updates_resource.apply(
      name=update_name, body={"action": "APPLY"}
  ).execute()
  op_name = operation.get("name")

  if not op_name or operation.get("done") is True:
    if "error" in operation:
      raise RuntimeError(
          f"ApplyWorkloadUpdate operation failed for '{update_name}':"
          f" {json.dumps(operation['error'])}"
      )
    res: dict[str, Any] = {
        "status": "APPLIED_WORKLOAD_UPDATE",
        "action": "apply",
        "workloadName": workload_name,
        "updateName": update_name,
        "updateId": update_id,
        "operationName": op_name,
        "operationDone": True,
    }
    applied_update = operation.get("response", {}).get("appliedUpdate")
    if applied_update is not None:
      res["appliedUpdate"] = applied_update
    if operation.get("metadata") is not None:
      res["operationMetadata"] = operation.get("metadata")
    return res

  deadline = time.monotonic() + poll_timeout_seconds
  latest_op = operation
  while time.monotonic() < deadline:
    time.sleep(poll_interval_seconds)
    latest_op = operations_resource.get(name=op_name).execute() or {}
    if latest_op.get("done") is True:
      if "error" in latest_op:
        raise RuntimeError(
            f"ApplyWorkloadUpdate operation '{op_name}' failed for"
            f" '{update_name}': {json.dumps(latest_op['error'])}"
        )
      res = {
          "status": "APPLIED_WORKLOAD_UPDATE",
          "action": "apply",
          "workloadName": workload_name,
          "updateName": update_name,
          "updateId": update_id,
          "operationName": op_name,
          "operationDone": True,
      }
      applied_update = latest_op.get("response", {}).get("appliedUpdate")
      if applied_update is not None:
        res["appliedUpdate"] = applied_update
      if latest_op.get("metadata") is not None:
        res["operationMetadata"] = latest_op.get("metadata")
      return res

  return {
      "status": "APPLY_OPERATION_IN_PROGRESS",
      "action": "apply",
      "workloadName": workload_name,
      "updateName": update_name,
      "updateId": update_id,
      "operationName": op_name,
      "operationDone": False,
      "message": (
          f"Operation '{op_name}' is still running after"
          f" {poll_timeout_seconds}s. Check status via 'gcloud assured"
          f" operations describe {op_name}'."
      ),
  }


def execute_manage_workload_updates(
    action: str,
    workload_id: str | None = None,
    organization: str | None = None,
    location: str | None = None,
    update_id: str | None = None,
    enable_compliance_updates: bool = False,
    include_all_states: bool = False,
    page_size: int = 50,
    poll_timeout_seconds: int = 180,
    poll_interval_seconds: int = 3,
    dry_run: bool = False,
    service: Any = None,
) -> dict[str, Any]:
  """Executes list, enable, or apply for Assured Workloads V1 configuration updates."""
  clean_action = action.strip().lower()
  (
      workload_name,
      clean_org,
      clean_loc,
      clean_wid,
      update_names,
      update_ids,
  ) = resolve_workload_and_update_names(
      action=clean_action,
      workload_id=workload_id,
      organization=organization,
      location=location,
      update_id=update_id,
  )

  if page_size < 1 or page_size > 100:
    raise ValueError(
        f"Invalid '--page-size' value '{page_size}'. Must be between 1 and 100."
    )
  if poll_timeout_seconds < 0:
    raise ValueError("--poll-timeout-seconds must be >= 0.")
  if poll_interval_seconds < 1:
    raise ValueError("--poll-interval-seconds must be >= 1.")

  regional_endpoint = f"https://{clean_loc}-assuredworkloads.googleapis.com"

  if dry_run:
    if clean_action == "list":
      return {
          "status": "DRY_RUN",
          "action": "list",
          "workloadName": workload_name,
          "organization": clean_org,
          "location": clean_loc,
          "workloadId": clean_wid,
          "regionalEndpoint": regional_endpoint,
          "userAgent": USER_AGENT,
          "enableComplianceUpdatesFirst": enable_compliance_updates,
          "request": {
              "method": (
                  "assuredworkloads.organizations.locations.workloads.updates.list"
              ),
              "parent": workload_name,
              "pageSize": page_size,
          },
      }
    if clean_action == "enable":
      return {
          "status": "DRY_RUN",
          "action": "enable",
          "workloadName": workload_name,
          "organization": clean_org,
          "location": clean_loc,
          "workloadId": clean_wid,
          "regionalEndpoint": regional_endpoint,
          "userAgent": USER_AGENT,
          "request": {
              "method": (
                  "assuredworkloads.organizations.locations.workloads.enableComplianceUpdates"
              ),
              "name": workload_name,
          },
      }
    if update_ids == ["ALL"]:
      return {
          "status": "DRY_RUN",
          "action": "apply",
          "workloadName": workload_name,
          "updateId": "ALL",
          "updateIds": ["ALL"],
          "organization": clean_org,
          "location": clean_loc,
          "workloadId": clean_wid,
          "regionalEndpoint": regional_endpoint,
          "userAgent": USER_AGENT,
          "request": {
              "method": (
                  "assuredworkloads.organizations.locations.workloads.updates.apply"
              ),
              "mode": "APPLY_ALL_AVAILABLE_SEQUENTIALLY",
              "parent": workload_name,
              "body": {"action": "APPLY"},
          },
      }
    assert update_names is not None and update_ids is not None
    if len(update_names) == 1:
      return {
          "status": "DRY_RUN",
          "action": "apply",
          "workloadName": workload_name,
          "updateName": update_names[0],
          "updateId": update_ids[0],
          "organization": clean_org,
          "location": clean_loc,
          "workloadId": clean_wid,
          "regionalEndpoint": regional_endpoint,
          "userAgent": USER_AGENT,
          "request": {
              "method": (
                  "assuredworkloads.organizations.locations.workloads.updates.apply"
              ),
              "name": update_names[0],
              "body": {"action": "APPLY"},
          },
      }
    return {
        "status": "DRY_RUN",
        "action": "apply",
        "workloadName": workload_name,
        "updateNames": update_names,
        "updateIds": update_ids,
        "organization": clean_org,
        "location": clean_loc,
        "workloadId": clean_wid,
        "regionalEndpoint": regional_endpoint,
        "userAgent": USER_AGENT,
        "request": {
            "method": (
                "assuredworkloads.organizations.locations.workloads.updates.apply"
            ),
            "names": update_names,
            "body": {"action": "APPLY"},
        },
    }

  if service is None:
    service = _create_discovery_service(clean_loc)

  workloads_resource = service.organizations().locations().workloads()

  if clean_action == "enable":
    workloads_resource.enableComplianceUpdates(name=workload_name).execute()
    return {
        "status": "ENABLED_COMPLIANCE_UPDATES",
        "action": "enable",
        "workloadName": workload_name,
        "regionalEndpoint": regional_endpoint,
    }

  updates_resource = workloads_resource.updates()

  if clean_action == "list":
    if enable_compliance_updates:
      workloads_resource.enableComplianceUpdates(name=workload_name).execute()

    all_updates, available_updates, state_counts = _fetch_all_updates(
        updates_resource, workload_name, page_size
    )
    result: dict[str, Any] = {
        "status": "LISTED_WORKLOAD_UPDATES",
        "action": "list",
        "workloadName": workload_name,
        "regionalEndpoint": regional_endpoint,
        "complianceUpdatesEnabledInRun": enable_compliance_updates,
        "stateCounts": state_counts,
        "availableUpdates": available_updates,
    }
    if include_all_states:
      result["allUpdates"] = all_updates
    return result

  # clean_action == "apply"
  operations_resource = service.organizations().locations().operations()

  if update_ids == ["ALL"]:
    _, available_updates, initial_counts = _fetch_all_updates(
        updates_resource, workload_name, page_size
    )
    if not available_updates:
      return {
          "status": "NO_AVAILABLE_UPDATES_TO_APPLY",
          "action": "apply",
          "workloadName": workload_name,
          "appliedCount": 0,
          "appliedUpdates": [],
          "stateCounts": initial_counts,
      }
    targets: list[tuple[str, str]] = []
    for u in available_updates:
      u_name = u.get("name", "")
      if u_name:
        targets.append((u_name, u_name.split("/")[-1]))
  else:
    assert update_names is not None and update_ids is not None
    targets = list(zip(update_names, update_ids))

  # Single update ID (preserve exact single-update output structure)
  if len(targets) == 1 and update_ids != ["ALL"]:
    u_name, u_id = targets[0]
    return _apply_single_update_and_poll(
        updates_resource=updates_resource,
        operations_resource=operations_resource,
        workload_name=workload_name,
        update_name=u_name,
        update_id=u_id,
        poll_timeout_seconds=poll_timeout_seconds,
        poll_interval_seconds=poll_interval_seconds,
    )

  # Multiple updates or --update-id=ALL: apply sequentially, then verify via list
  applied_results: list[dict[str, Any]] = []
  for u_name, u_id in targets:
    single_res = _apply_single_update_and_poll(
        updates_resource=updates_resource,
        operations_resource=operations_resource,
        workload_name=workload_name,
        update_name=u_name,
        update_id=u_id,
        poll_timeout_seconds=poll_timeout_seconds,
        poll_interval_seconds=poll_interval_seconds,
    )
    applied_results.append(single_res)

  _, remaining_available, final_state_counts = _fetch_all_updates(
      updates_resource, workload_name, page_size
  )
  all_done = all(r.get("operationDone") is True for r in applied_results)
  return {
      "status": (
          "APPLIED_WORKLOAD_UPDATES"
          if all_done
          else "APPLY_OPERATIONS_IN_PROGRESS"
      ),
      "action": "apply",
      "workloadName": workload_name,
      "appliedCount": sum(
          1 for r in applied_results if r.get("operationDone") is True
      ),
      "totalRequested": len(targets),
      "allOperationsDone": all_done,
      "appliedUpdates": applied_results,
      "postApplyStateCounts": final_state_counts,
      "remainingAvailableUpdates": remaining_available,
  }


def build_arg_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(
      description=(
          "List, enable, or apply Assured Workloads V1 configuration updates"
          " via google-api-python-client."
      )
  )
  parser.add_argument(
      "--action",
      default="list",
      choices=["list", "enable", "apply"],
      help=(
          "Update action: 'list' available updates (default), 'enable'"
          " compliance updates, or 'apply' update(s)."
      ),
  )
  parser.add_argument(
      "--workload-id",
      default=None,
      help=(
          "Workload ID or full resource name"
          " (organizations/<ORG>/locations/<LOC>/workloads/<ID>)."
      ),
  )
  parser.add_argument(
      "--organization",
      default=None,
      help="Numeric Organization ID (optional if full resource name is passed).",
  )
  parser.add_argument(
      "--location",
      default=None,
      help=(
          "Regional or multi-regional location, e.g., us-central1, us, eu"
          " (optional if full resource name is passed)."
      ),
  )
  parser.add_argument(
      "--update-id",
      default=None,
      help=(
          "Update ID, comma-separated Update IDs (<ID1>,<ID2>), 'ALL' (to apply"
          " all AVAILABLE updates sequentially), or full update resource name"
          " (organizations/<ORG>/locations/<LOC>/workloads/<WID>/updates/<UID>)"
          " required when --action=apply."
      ),
  )
  parser.add_argument(
      "--enable-compliance-updates",
      action="store_true",
      help=(
          "Call enableComplianceUpdates on the workload before listing updates"
          " (useful for existing folders where compliance updates are not yet"
          " enabled)."
      ),
  )
  parser.add_argument(
      "--include-all-states",
      action="store_true",
      help=(
          "Include APPLIED and WITHDRAWN updates in addition to AVAILABLE"
          " updates when --action=list."
      ),
  )
  parser.add_argument(
      "--page-size",
      type=int,
      default=50,
      help="Page size for updates.list (1-100, default: 50).",
  )
  parser.add_argument(
      "--poll-timeout-seconds",
      type=int,
      default=180,
      help=(
          "Maximum seconds to poll each ApplyWorkloadUpdate LRO until"
          " completion (default: 180)."
      ),
  )
  parser.add_argument(
      "--poll-interval-seconds",
      type=int,
      default=3,
      help="Seconds between LRO status checks when --action=apply (default: 3).",
  )
  parser.add_argument(
      "--dry-run",
      action="store_true",
      help=(
          "Validate arguments and print the request details without calling the"
          " API."
      ),
  )
  return parser


def main(argv: list[str] | None = None) -> int:
  parser = build_arg_parser()
  args = parser.parse_args(argv)
  try:
    result = execute_manage_workload_updates(
        action=args.action,
        workload_id=args.workload_id,
        organization=args.organization,
        location=args.location,
        update_id=args.update_id,
        enable_compliance_updates=args.enable_compliance_updates,
        include_all_states=args.include_all_states,
        page_size=args.page_size,
        poll_timeout_seconds=args.poll_timeout_seconds,
        poll_interval_seconds=args.poll_interval_seconds,
        dry_run=args.dry_run,
    )
    print(json.dumps(result, indent=2))
    return 0
  except (ValueError, RuntimeError) as err:
    sys.stderr.write(f"MANAGE_WORKLOAD_UPDATES_ERROR: {err}\n")
    return 1
  except Exception as err:  # pylint: disable=broad-exception-caught
    sys.stderr.write(f"MANAGE_WORKLOAD_UPDATES_ERROR: {err}\n")
    return 1


if __name__ == "__main__":
  sys.exit(main())
