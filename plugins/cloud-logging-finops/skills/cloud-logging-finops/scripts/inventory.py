"""Log Router, flow log and log read scope inventory.

Every fetch reports what it could not read (an `unavailable` list, or the read
scope's `note`), so a project the skill lacked access to inspect is not
reported as one with nothing to clean up or no logs to sample.
"""

from typing import Any, Dict, Iterator, List, Optional, Tuple

import attribution

_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)


def authed_session() -> Any:
  """Returns an authorized, attributed requests session; raises without ADC."""
  import google.auth  # pylint: disable=g-import-not-at-top
  from google.auth.transport import requests as auth_requests  # pylint: disable=g-import-not-at-top

  credentials, _ = google.auth.default(scopes=list(_SCOPES))
  return attribution.tag_session(
      auth_requests.AuthorizedSession(credentials),
      attribution.COLLECT_LOGGING_DATA,
  )


def _pages(
    session: Any,
    url: str,
    params: Dict[str, Any],
    what: str,
    timeout: int,
    unavailable: List[str],
) -> Iterator[Dict[str, Any]]:
  """Yields each page of a Google REST list call, following `nextPageToken`."""
  # A failed page ends the listing and is recorded in `unavailable`; the pages
  # already yielded are kept.
  page_token = None
  while True:
    try:
      response = session.get(
          url, params={**params, "pageToken": page_token}, timeout=timeout
      )
      if not response.ok:
        raise RuntimeError(f"HTTP {response.status_code}")
      payload = response.json()
    except Exception as e:  # pylint: disable=broad-except
      print(f"Notice: unable to list {what}: {e}")
      unavailable.append(f"{what}: {e}")
      return
    yield payload
    page_token = payload.get("nextPageToken")
    if not page_token:
      return


def fetch_log_router_inventory(
    session: Any, project_id: str
) -> Tuple[Dict[str, List[Any]], List[str]]:
  """Fetches Log Router sinks and exclusions (project-level and sink-attached).

  Exclusions record operator intent that their volume should be dropped.

  Args:
    session: authorized `requests.Session`.
    project_id: project to read.

  Returns:
    `({"sinks": [...], "exclusions": [...]}, unavailable)`.
  """
  base = f"https://logging.googleapis.com/v2/projects/{project_id}"
  out: Dict[str, List[Any]] = {"sinks": [], "exclusions": []}
  unavailable: List[str] = []
  for key in out:
    for page in _pages(
        session, f"{base}/{key}", {}, f"Log Router {key}", 60, unavailable
    ):
      out[key].extend(page.get(key) or [])

  seen = {x.get("name") for x in out["exclusions"]}
  for sink in out["sinks"]:
    for exclusion in sink.get("exclusions") or []:
      if exclusion.get("name") not in seen:
        seen.add(exclusion.get("name"))
        out["exclusions"].append(exclusion)
  return out, unavailable


def fetch_flow_log_configs(
    session: Any, project_id: str
) -> Tuple[List[Dict[str, Any]], List[str]]:
  """Fetches VPC flow log configs from both managing APIs.

  Network Management and per-subnet Compute configs emit different log IDs, so
  both are needed.

  Args:
    session: authorized `requests.Session`.
    project_id: project to read.

  Returns:
    `([{"state", "flow_sampling"}, ...], unavailable)`.
  """
  configs: List[Dict[str, Any]] = []
  unavailable: List[str] = []

  for page in _pages(
      session,
      "https://networkmanagement.googleapis.com/v1/projects/"
      f"{project_id}/locations/global/vpcFlowLogsConfigs",
      {"pageSize": 500},
      "VPC flow log configs",
      60,
      unavailable,
  ):
    for cfg in page.get("vpcFlowLogsConfigs") or []:
      configs.append(
          {"state": cfg.get("state"), "flow_sampling": cfg.get("flowSampling")}
      )

  for page in _pages(
      session,
      "https://compute.googleapis.com/compute/v1/projects/"
      f"{project_id}/aggregated/subnetworks",
      {"maxResults": 500},
      "subnet flow log configs",
      120,
      unavailable,
  ):
    for scoped in (page.get("items") or {}).values():
      for subnet in scoped.get("subnetworks") or []:
        log_config = subnet.get("logConfig") or {}
        if log_config.get("enable"):
          configs.append({
              "state": "ENABLED",
              "flow_sampling": log_config.get("flowSampling"),
          })

  return configs, unavailable


_DEFAULT_SCOPE_URL = (
    "https://observability.googleapis.com/v1/projects/{project_id}"
    "/locations/global/scopes/_Default"
)
_LOGGING_V2 = "https://logging.googleapis.com/v2/"
# `Scope.logScope` carries the service prefix; the Logging API path does not.
_LOG_SCOPE_PREFIX = "logging.googleapis.com/"


def project_read_scope(
    project_id: str, note: Optional[str] = None
) -> Dict[str, Any]:
  """The read scope that covers only the project's own buckets."""
  scope: Dict[str, Any] = {
      "source": "project",
      "log_scope": None,
      "resource_names": [f"projects/{project_id}"],
  }
  if note:
    scope["note"] = note
  return scope


def resolve_log_read_scope(session: Any, project_id: str) -> Dict[str, Any]:
  """Returns the resources to read log entries from, as Logs Explorer would.

  Logs Explorer reads through the project's default observability scope, whose
  log scope may list log views in other buckets or projects instead of the
  project itself. Reading only `projects/{id}` then returns nothing even though
  the user can see the logs. Any failure falls back to the project alone and is
  recorded in `note`, so an unresolved scope is disclosed rather than read as
  "no logs".

  Args:
    session: authorized `requests.Session`, or None.
    project_id: project whose default scope is read.

  Returns:
    `{"source": "default_scope" | "project", "log_scope", "resource_names"}`,
    plus `note` when the fallback was used.
  """
  if session is None:
    return project_read_scope(project_id, "no authorized session")

  def get_json(url: str, what: str) -> Dict[str, Any]:
    response = session.get(url, params={}, timeout=30)
    if not response.ok:
      raise RuntimeError(f"{what}: HTTP {response.status_code}")
    return response.json() or {}

  try:
    scope = get_json(
        _DEFAULT_SCOPE_URL.format(project_id=project_id),
        "default observability scope",
    )
    log_scope = str(scope.get("logScope") or "")
    if log_scope.startswith(_LOG_SCOPE_PREFIX):
      log_scope = log_scope[len(_LOG_SCOPE_PREFIX):]
    if not log_scope:
      return project_read_scope(
          project_id, "the default observability scope names no log scope"
      )
    resources = get_json(_LOGGING_V2 + log_scope, f"log scope {log_scope}").get(
        "resourceNames"
    ) or []
  except Exception as e:  # pylint: disable=broad-except
    print(
        "Notice: unable to resolve the default log scope; reading"
        f" projects/{project_id} only: {e}"
    )
    return project_read_scope(project_id, str(e))

  if not resources:
    scope = project_read_scope(project_id, "the log scope lists no resources")
    scope["log_scope"] = log_scope
    return scope
  return {
      "source": "default_scope",
      "log_scope": log_scope,
      # Order kept; a repeated resource would only duplicate samples.
      "resource_names": list(dict.fromkeys(resources)),
  }
