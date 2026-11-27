"""Loads Data Boundary BUILT_IN and org CUSTOM resources via the gcloud CLI.

Runs the read-only `gcloud compliance-manager frameworks list` and
`gcloud compliance-manager cloud-controls list` commands for an organization
and a location, and caches the filtered result for the session.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import time
from typing import Any, Literal

DEFAULT_CACHE_DIR = os.path.join(
    tempfile.gettempdir(),
    "db_framework_navigator",
)
# The location used when the customer names none.
DEFAULT_LOCATION = "global"
# The supported location IDs, each with a plain-words description. The path is
# not resolved through symbolic links: a build system can link each file on its
# own, and following the link would lose the neighbouring `assets/` directory.
LOCATIONS_FILE = (
    pathlib.Path(os.path.abspath(__file__)).parent.parent
    / "assets"
    / "locations.json"
)
GCLOUD_TIMEOUT_SECONDS = 120
# gcloud's default page size returned incomplete lists for this API, so ask for
# one large page.
GCLOUD_PAGE_SIZE = 1000
# Built-in frameworks that are kept although they lack the ASSURED_WORKLOADS
# category.
_EXTRA_BUILTIN_FRAMEWORK_IDS = frozenset({"builtin-hipaa"})
_MAX_ERROR_CHARS = 800
_ORGANIZATION_ID_RE = re.compile(r"[0-9]+")


class GcloudError(Exception):
  """Raised when a gcloud invocation fails or returns unusable output."""


@dataclasses.dataclass
class DBResourcesStore:
  """Container for active Data Boundary BUILT_IN and org CUSTOM resources."""

  last_synced_epoch: float
  organization_id: str = ""
  frameworks: dict[str, dict[str, Any]] = dataclasses.field(
      default_factory=dict
  )
  cloud_controls: dict[str, dict[str, Any]] = dataclasses.field(
      default_factory=dict
  )
  location: str = DEFAULT_LOCATION

  def to_json(self) -> str:
    return json.dumps(dataclasses.asdict(self), indent=2)

  @classmethod
  def from_dict(cls, data: dict[str, Any]) -> DBResourcesStore:
    epoch = data.get("last_synced_epoch", data.get("last_compiled_epoch", 0.0))
    return cls(
        last_synced_epoch=float(epoch),
        organization_id=str(data.get("organization_id", "")),
        frameworks=dict(data.get("frameworks", {})),
        cloud_controls=dict(data.get("cloud_controls", {})),
        # A cache file written before locations existed counts as `global`.
        location=str(data.get("location", DEFAULT_LOCATION)),
    )


def normalize_organization_id(raw: str) -> str:
  """Returns the numeric organization ID; accepts `organizations/<ID>` too."""
  org_id = raw.strip()
  if org_id.startswith("organizations/"):
    org_id = org_id[len("organizations/") :]
  if not _ORGANIZATION_ID_RE.fullmatch(org_id):
    raise ValueError(
        f"Invalid organization ID {raw!r}: expected the numeric organization"
        " ID."
    )
  return org_id


def load_locations(path: pathlib.Path = LOCATIONS_FILE) -> dict[str, str]:
  """Returns the supported locations as a map from location ID to description.

  Args:
    path: The JSON file that lists the supported locations.

  Raises:
    ValueError: If the file is missing or does not have the expected shape.
  """
  try:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {entry["id"]: entry["description"] for entry in data["locations"]}
  except (OSError, ValueError, KeyError, TypeError) as e:
    raise ValueError(
        f"Could not read the supported locations from {path.name}: {e!r}"
    ) from e


def normalize_location(raw: str) -> str:
  """Returns the location ID if it is one of the supported locations.

  The match is exact: no case folding, no prefix handling, no guessing.

  Args:
    raw: The location ID as given on the command line.

  Raises:
    ValueError: If the ID is not in the list of supported locations.
  """
  location = raw.strip()
  if location not in load_locations():
    raise ValueError(
        f"Unknown location {raw!r}: use one of the location IDs in"
        f" {LOCATIONS_FILE.name} (default: {DEFAULT_LOCATION})."
    )
  return location


def _summarize_stderr(stderr: str) -> str:
  """Returns the actionable part of gcloud's stderr.

  gcloud can append very large debug traces to its `ERROR:` line, and prints
  informational lines such as "Parsed [location] resource" even on success. The
  `ERROR:` prefix is dropped because the caller adds its own.

  Args:
    stderr: The raw stderr of a failed gcloud invocation.
  """
  lines = [line.strip() for line in stderr.splitlines() if line.strip()]
  for line in lines:
    if line.startswith("ERROR:"):
      return line[len("ERROR:") :].strip()[:_MAX_ERROR_CHARS]
  return " ".join(lines[:3])[:_MAX_ERROR_CHARS]


def run_gcloud_list(
    resource_kind: Literal["frameworks", "cloud-controls"],
    organization_id: str,
    location: str = DEFAULT_LOCATION,
) -> list[dict[str, Any]]:
  """Lists every framework or cloud control of an organization via gcloud.

  Asks for pages of `GCLOUD_PAGE_SIZE` items, because gcloud's default page size
  returned incomplete lists for this API. A list of exactly one full page may
  still be incomplete, so the function warns on stderr in that case.

  Args:
    resource_kind: The `gcloud compliance-manager` command group to list.
    organization_id: The numeric Google Cloud organization ID.
    location: The location ID to list in.

  Returns:
    The parsed `--format=json` output: one dict per resource.

  Raises:
    GcloudError: If gcloud is missing, times out, exits non-zero, or prints
      something other than a JSON list.
  """
  command = [
      "gcloud",
      "compliance-manager",
      resource_kind,
      "list",
      f"--organization={organization_id}",
      f"--location={location}",
      f"--page-size={GCLOUD_PAGE_SIZE}",
      "--format=json",
      "--quiet",
  ]
  description = f"`gcloud compliance-manager {resource_kind} list`"
  try:
    result = subprocess.run(
        command,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        stdin=subprocess.DEVNULL,
        timeout=GCLOUD_TIMEOUT_SECONDS,
    )
  except FileNotFoundError as e:
    raise GcloudError(
        "The gcloud CLI was not found on PATH. Install the gcloud CLI and run"
        " `gcloud auth login`."
    ) from e
  except OSError as e:
    # For example PermissionError when gcloud exists but cannot be executed.
    raise GcloudError(f"Could not run the gcloud CLI: {e}") from e
  except subprocess.TimeoutExpired as e:
    raise GcloudError(
        f"{description} timed out after {GCLOUD_TIMEOUT_SECONDS} seconds."
    ) from e

  if result.returncode != 0:
    raise GcloudError(
        f"{description} failed (exit code {result.returncode}):"
        f" {_summarize_stderr(result.stderr)}"
    )
  try:
    items = json.loads(result.stdout)
  except json.JSONDecodeError as e:
    raise GcloudError(f"{description} did not return valid JSON.") from e
  if not isinstance(items, list):
    raise GcloudError(f"{description} did not return a JSON list.")
  if len(items) == GCLOUD_PAGE_SIZE:
    print(
        f"WARNING: {description} returned exactly {GCLOUD_PAGE_SIZE} items,"
        " one full page, so the list may be incomplete.",
        file=sys.stderr,
    )
  return items


def fetch_and_filter_db_resources(
    organization_id: str, location: str = DEFAULT_LOCATION
) -> DBResourcesStore:
  """Fetches all FWs & CCs in one pass, filtering BUILT_IN and keeping CUSTOM."""
  raw_fws = run_gcloud_list("frameworks", organization_id, location)
  raw_ccs = run_gcloud_list("cloud-controls", organization_id, location)

  frameworks_by_id: dict[str, dict[str, Any]] = {}
  underlying_db_cc_ids: set[str] = set()

  for fw in raw_fws:
    fw_id = fw.get("name", "").split("/")[-1]
    if not fw_id:
      continue
    is_builtin = fw_id.startswith("builtin-")
    fw_item = dict(fw)

    if is_builtin:
      categories = fw_item.get("category", [])
      if (
          "ASSURED_WORKLOADS" not in categories
          and fw_id not in _EXTRA_BUILTIN_FRAMEWORK_IDS
      ):
        continue
      for cc_ref in fw_item.get("cloudControlDetails", []):
        ref_id = cc_ref.get("name", "").split("/")[-1]
        if ref_id:
          underlying_db_cc_ids.add(ref_id)
    else:
      # Keep all Organization Custom Frameworks
      pass

    frameworks_by_id[fw_id] = fw_item

  cloud_controls_by_id: dict[str, dict[str, Any]] = {}
  for cc in raw_ccs:
    cc_id = cc.get("name", "").split("/")[-1]
    if not cc_id:
      continue
    is_builtin = cc_id.startswith("builtin-")
    cc_item = dict(cc)

    if is_builtin and cc_id not in underlying_db_cc_ids:
      continue

    cloud_controls_by_id[cc_id] = cc_item

  return DBResourcesStore(
      last_synced_epoch=time.time(),
      organization_id=organization_id,
      frameworks=frameworks_by_id,
      cloud_controls=cloud_controls_by_id,
      location=location,
  )


def _cache_file_name(organization_id: str, location: str) -> str:
  """Returns the cache file name; `global` keeps the name without a suffix."""
  if location == DEFAULT_LOCATION:
    return f"db_resources_cache_{organization_id}.json"
  return f"db_resources_cache_{organization_id}_{location}.json"


def load_db_resources(
    organization_id: str,
    cache_dir: str = DEFAULT_CACHE_DIR,
    refresh_cache: bool = False,
    location: str = DEFAULT_LOCATION,
) -> DBResourcesStore:
  """Loads DB BUILT_IN + org CUSTOM resources from the session cache or gcloud."""
  organization_id = normalize_organization_id(organization_id)
  location = normalize_location(location)
  cache_file = pathlib.Path(cache_dir) / _cache_file_name(
      organization_id, location
  )

  if not refresh_cache and cache_file.exists():
    loaded = DBResourcesStore.from_dict(json.loads(cache_file.read_text()))
    if (
        loaded.location == location
        and loaded.frameworks
        and loaded.cloud_controls
    ):
      return loaded

  store = fetch_and_filter_db_resources(organization_id, location)
  cache_file.parent.mkdir(parents=True, exist_ok=True)
  cache_file.write_text(store.to_json())
  return store


def main() -> None:
  parser = argparse.ArgumentParser(description="Load Data Boundary Resources")
  parser.add_argument(
      "-o", "--organization_id", required=True, help="GCP Organization ID"
  )
  parser.add_argument(
      "--output_path",
      required=True,
      help=(
          "Path to save the loaded database of DB frameworks and cloud"
          " controls."
      ),
  )
  parser.add_argument(
      "--location",
      default=DEFAULT_LOCATION,
      help=(
          "Location ID from the list of supported locations (default:"
          f" {DEFAULT_LOCATION})."
      ),
  )
  parser.add_argument(
      "--cache_dir",
      default=DEFAULT_CACHE_DIR,
      help="Directory to store per-session caches.",
  )
  parser.add_argument(
      "--refresh_cache",
      action="store_true",
      help="Force a refresh from gcloud even if a cache file exists.",
  )
  args = parser.parse_args()

  try:
    store = load_db_resources(
        args.organization_id, args.cache_dir, args.refresh_cache, args.location
    )
  except (GcloudError, ValueError) as e:
    print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)

  out_path = pathlib.Path(args.output_path)
  out_path.parent.mkdir(parents=True, exist_ok=True)
  out_path.write_text(store.to_json())
  print(
      f"Successfully loaded and saved {len(store.frameworks)} frameworks and"
      f" {len(store.cloud_controls)} cloud controls to {args.output_path}"
  )


if __name__ == "__main__":
  main()
