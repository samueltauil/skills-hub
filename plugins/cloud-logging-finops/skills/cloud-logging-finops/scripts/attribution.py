"""Usage attribution for the Google Cloud API requests this skill sends.

Prefixes `google-skills/1.0 (skill:cloud-logging-finops; script:<script>)` to
the `User-Agent` (HTTP/JSON) or `x-goog-api-client` (gRPC) header. The token
carries no project, user, or request data.
"""

from typing import Any

SKILL_NAME = "cloud-logging-finops"

# Version of the token format the usage analytics parse, not of this skill.
_TOKEN_FORMAT_VERSION = "1.0"

# Script names as they appear in the token. Library modules (billing,
# inventory, analytics, ...) only run inside `collect_logging_data.py`, so they
# attribute their requests to it.
COLLECT_LOGGING_DATA = "collect-logging-data"
VERIFY_CLAIM = "verify-claim"


def user_agent(script: str) -> str:
  """Returns the attribution token for requests sent by `script`."""
  return (
      f"google-skills/{_TOKEN_FORMAT_VERSION}"
      f" (skill:{SKILL_NAME}; script:{script})"
  )


def _prefixed(token: str, existing: Any) -> str:
  return f"{token} {existing}" if existing else token


def client_info(script: str) -> Any:
  """Returns a ClientInfo that tags every request a client sends."""
  # Works for both GAPIC and HTTP/JSON clients (it subclasses the base one).
  from google.api_core.gapic_v1 import client_info as gapic_client_info  # pylint: disable=g-import-not-at-top

  return gapic_client_info.ClientInfo(user_agent=user_agent(script))


def tag_session(session: Any, script: str) -> Any:
  """Prefixes the token to a `requests.Session`'s User-Agent; returns it."""
  session.headers["User-Agent"] = _prefixed(
      user_agent(script), session.headers.get("User-Agent")
  )
  return session


def discovery_request_builder(script: str) -> Any:
  """Returns a `requestBuilder` for `googleapiclient.discovery.build`."""
  # Discovery clients take no user-agent option; `requestBuilder` builds every
  # request, including `list_next` pages.
  from googleapiclient import http as googleapiclient_http  # pylint: disable=g-import-not-at-top

  token = user_agent(script)

  class _AttributedHttpRequest(googleapiclient_http.HttpRequest):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
      headers = dict(kwargs.get("headers") or {})
      headers["user-agent"] = _prefixed(token, headers.get("user-agent"))
      kwargs["headers"] = headers
      super().__init__(*args, **kwargs)

  return _AttributedHttpRequest
