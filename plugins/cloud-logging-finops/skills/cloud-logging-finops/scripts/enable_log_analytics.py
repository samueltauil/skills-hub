"""Enables Log Analytics on a Google Cloud Logging bucket."""

from collections.abc import Sequence
import sys
from typing import Any, Dict

from absl import app
from absl import flags
from google.api_core import exceptions as api_exceptions
from google.api_core.gapic_v1 import client_info as gapic_client_info
from google.cloud.logging_v2 import types as logging_types
from google.cloud.logging_v2.services import config_service_v2

ConfigServiceV2Client = config_service_v2.ConfigServiceV2Client
LogBucket = logging_types.LogBucket
UpdateBucketRequest = logging_types.UpdateBucketRequest

# Attribution token (see `attribution.py`), duplicated because this strict-deps
# target cannot import that sibling module.
USER_AGENT = (
    "google-skills/1.0"
    " (skill:cloud-logging-finops; script:enable-log-analytics)"
)
# gcloud only takes a custom User-Agent through this variable, and needs the
# product name ahead of the token.
GCLOUD_METRICS_ENVIRONMENT = f"google-skills {USER_AGENT}"

FLAGS = flags.FLAGS
if "project-id" not in FLAGS:
  flags.DEFINE_string("project-id", None, "GCP Project ID.")
if "bucket-id" not in FLAGS:
  flags.DEFINE_string(
      "bucket-id", "_Default", "Bucket ID to enable Log Analytics on."
  )
if "location" not in FLAGS:
  flags.DEFINE_string("location", "global", "Bucket GCP location.")


def enable_log_analytics(
    config_client: ConfigServiceV2Client,
    project_id: str,
    bucket_id: str = "_Default",
    location: str = "global",
) -> Dict[str, Any]:
  """Enables Log Analytics on the specified bucket."""
  bucket_name = (
      f"projects/{project_id}/locations/{location}/buckets/{bucket_id}"
  )
  bucket = LogBucket(name=bucket_name, analytics_enabled=True)
  # proto-plus builds the FieldMask from a dict, so no protobuf import is
  # needed.
  mask = {"paths": ["analytics_enabled"]}
  request = UpdateBucketRequest(
      name=bucket_name, bucket=bucket, update_mask=mask
  )

  try:
    updated = config_client.update_bucket(request=request)
  except api_exceptions.GoogleAPICallError as e:
    if isinstance(e, api_exceptions.NotFound):
      diagnostic = (
          f"Bucket '{bucket_name}' was not found. Verify project ID, bucket"
          " ID, and location."
      )
    else:
      diagnostic = (
          "Ensure your identity has 'roles/logging.admin' or"
          " 'roles/logging.configWriter'."
      )
    return {
        "success": False,
        "bucket": bucket_name,
        "error": str(e),
        "message": (
            f"Failed to enable Log Analytics on '{bucket_name}': {e}.\n"
            f"  - Action: {diagnostic}\n"
            "  - Alternatively, run via gcloud CLI:\n"
            f'      CLOUDSDK_METRICS_ENVIRONMENT="{GCLOUD_METRICS_ENVIRONMENT}"'
            f" gcloud logging buckets update {bucket_id}"
            f" --location={location} --project={project_id} --enable-analytics"
        ),
    }
  if updated.analytics_enabled:
    message = (
        f"Successfully enabled Log Analytics on '{bucket_name}'.\n  - New"
        " logs will be queryable via SQL immediately.\n  - Historical logs"
        " prior to enablement are not retroactively indexed for SQL.\n  -"
        " Recommendation: Wait ~1 to 2 hours for a representative traffic"
        " sample before re-running audit."
    )
  else:
    message = (
        f"'{bucket_name}' was updated but still reports Log Analytics"
        " disabled."
    )
  return {
      "success": updated.analytics_enabled,
      "bucket": bucket_name,
      "analytics_enabled": updated.analytics_enabled,
      "message": message,
  }


def main(argv: Sequence[str]) -> None:
  if len(argv) > 1:
    raise app.UsageError("Too many command-line arguments.")
  project_id = FLAGS["project-id"].value
  if not project_id:
    raise app.UsageError("Flag --project-id is required.")

  client = ConfigServiceV2Client(
      client_info=gapic_client_info.ClientInfo(user_agent=USER_AGENT)
  )
  res = enable_log_analytics(
      client,
      project_id,
      FLAGS["bucket-id"].value or "_Default",
      FLAGS["location"].value or "global",
  )
  if res["success"]:
    print(res["message"])
  else:
    print(res["message"], file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
  app.run(main)
