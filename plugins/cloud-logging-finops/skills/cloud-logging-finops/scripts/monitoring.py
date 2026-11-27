"""Cloud Monitoring (GCM) metric queries and parsing.

Buckets are aligned to UTC midnight so they are calendar days, and a failed
query is reported as a missing window, never as zero volume.
"""

import collections
import concurrent.futures
import datetime
from typing import Any, Dict, List, NamedTuple, Sequence, Tuple

from constants import BILLED_BYTES_METRIC
from constants import BYTE_COUNT_METRIC
from constants import DEFAULT_SAMPLE_DAYS
from constants import MONITORING_RETENTION_DAYS
from google.api_core import exceptions as api_exceptions
from google.cloud import monitoring_v3

_ALIGNMENT_SECONDS = 86400

# Short so a too-wide window fails fast enough to be halved and retried.
_CHUNK_TIMEOUT_SECONDS = 60.0

# Series are day-aligned, so splitting below one day cannot help.
_MIN_CHUNK_DAYS = 1

_MAX_WORKERS = 12

_BYTE_COUNT = f'metric.type = "{BYTE_COUNT_METRIC}"'

# An empty severity label is what the Log Router calls DEFAULT.
DEFAULT_SEVERITY = "DEFAULT"


class SeriesResult(NamedTuple):
  """Time series plus the windows that could not be fetched.

  Non-empty `missing_windows` means the series is a lower bound.
  """

  series: List[Any]
  missing_windows: List[str]


def floor_to_utc_day(moment: datetime.datetime) -> datetime.datetime:
  """Truncates `moment` to midnight UTC, attaching UTC if it is naive."""
  if moment.tzinfo is None:
    moment = moment.replace(tzinfo=datetime.timezone.utc)
  return moment.astimezone(datetime.timezone.utc).replace(
      hour=0, minute=0, second=0, microsecond=0
  )


def _interval(
    end: datetime.datetime, newer_days: int, older_days: int
) -> monitoring_v3.TimeInterval:
  """The window from `older_days` to `newer_days` before `end`."""
  return monitoring_v3.TimeInterval({
      "end_time": {
          "seconds": int(
              (end - datetime.timedelta(days=newer_days)).timestamp()
          )
      },
      "start_time": {
          "seconds": int(
              (end - datetime.timedelta(days=older_days)).timestamp()
          )
      },
  })


def get_query_interval(
    now: datetime.datetime, lookback_days: int = MONITORING_RETENTION_DAYS
) -> monitoring_v3.TimeInterval:
  """Returns whole days ending at the most recent UTC midnight."""
  # The partial current day is excluded, and the span is clamped to Cloud
  # Monitoring's 42-day retention (longer requests silently return less).
  return _interval(
      floor_to_utc_day(now), 0, min(lookback_days, MONITORING_RETENTION_DAYS)
  )


def _query_time_series(
    client: monitoring_v3.MetricServiceClient,
    project_id: str,
    filter_str: str,
    interval: monitoring_v3.TimeInterval,
    group_by_fields: List[str],
    timeout: float = 180.0,
) -> List[Any]:
  """Queries GCM list_time_series with daily alignment."""
  results = client.list_time_series(
      request={
          "name": f"projects/{project_id}",
          "filter": filter_str,
          "interval": interval,
          "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
          "aggregation": monitoring_v3.Aggregation({
              "alignment_period": {"seconds": _ALIGNMENT_SECONDS},
              "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_SUM,
              "cross_series_reducer": (
                  monitoring_v3.Aggregation.Reducer.REDUCE_SUM
              ),
              "group_by_fields": group_by_fields,
          }),
      },
      timeout=timeout,
  )
  return list(results)


# Wide `byte_count` windows on chatty projects time out with 503/504 "Please
# shorten the time interval"; such windows are halved and retried.
_TIMEOUT_MARKERS = ("timed out", "shorten the time interval", "deadline")


def _is_timeout(error: Exception) -> bool:
  """Reports whether an error is the backend asking for a smaller window."""
  if isinstance(
      error,
      (
          api_exceptions.DeadlineExceeded,
          api_exceptions.ServiceUnavailable,
          api_exceptions.GatewayTimeout,
          api_exceptions.RetryError,
      ),
  ):
    return True
  message = str(error).lower()
  return any(marker in message for marker in _TIMEOUT_MARKERS)


def query_log_volume(
    client: monitoring_v3.MetricServiceClient,
    project_id: str,
    interval: monitoring_v3.TimeInterval,
) -> List[Any]:
  """Queries GCM for billed logging volume, grouped by resource type."""
  return _query_time_series(
      client=client,
      project_id=project_id,
      filter_str=f'metric.type = "{BILLED_BYTES_METRIC}"',
      interval=interval,
      group_by_fields=["metric.label.resource_type"],
  )


def _fetch_window(
    client: monitoring_v3.MetricServiceClient,
    project_id: str,
    group_by: List[str],
    flt: str,
    name: str,
    end: datetime.datetime,
    newer_days: int,
    older_days: int,
) -> Tuple[List[Any], List[str]]:
  """Fetches one `byte_count` window, halving it while the backend times out."""
  # Returns `(series, failed_windows)`. Only a single day that fails on its
  # own, or a non-timeout error, is reported as a gap.
  window = f"{name}[{newer_days}..{older_days}d]"
  try:
    return (
        _query_time_series(
            client=client,
            project_id=project_id,
            filter_str=flt,
            interval=_interval(end, newer_days, older_days),
            group_by_fields=group_by,
            timeout=_CHUNK_TIMEOUT_SECONDS,
        ),
        [],
    )
  except api_exceptions.InvalidArgument:
    # Grouping unsupported for this resource type: a genuine absence, not a gap.
    return [], []
  except (api_exceptions.GoogleAPICallError, api_exceptions.RetryError) as e:
    span = older_days - newer_days
    if span <= _MIN_CHUNK_DAYS or not _is_timeout(e):
      print(f"Warning: byte_count query {window} failed: {e}")
      return [], [window]
    midpoint = newer_days + span // 2
    print(f"Notice: {window} exceeded the backend's limit; splitting.")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
      halves = [
          executor.submit(
              _fetch_window,
              client,
              project_id,
              group_by,
              flt,
              name,
              end,
              lo,
              hi,
          )
          for lo, hi in ((newer_days, midpoint), (midpoint, older_days))
      ]
      series: List[Any] = []
      failures: List[str] = []
      for half in halves:
        half_series, half_missing = half.result()
        series.extend(half_series)
        failures.extend(half_missing)
    return series, failures


def _fetch_windowed(
    client: monitoring_v3.MetricServiceClient,
    project_id: str,
    group_by: List[str],
    now: datetime.datetime,
    days: int,
    chunk_days: int,
    scopes: Sequence[Tuple[str, str]],
) -> SeriesResult:
  """Fetches `byte_count` over `days` in parallel `chunk_days` windows.

  Args:
    client: Cloud Monitoring client.
    project_id: Project whose metrics are queried.
    group_by: Labels to group by.
    now: Reference instant; the window ends at the preceding UTC midnight.
    days: Width of the window, clamped to Cloud Monitoring's retention.
    chunk_days: Width of each parallel request.
    scopes: `(name, filter)` pairs, each fetched over the whole window; `name`
      labels its missing windows.

  Returns:
    The series of every scope, with any window that failed.
  """
  end = floor_to_utc_day(now)
  days = max(1, min(int(days), MONITORING_RETENTION_DAYS))
  results: List[Any] = []
  missing: List[str] = []
  with concurrent.futures.ThreadPoolExecutor(
      max_workers=_MAX_WORKERS
  ) as executor:
    tasks = []
    for name, flt in scopes:
      for newer in range(0, days, chunk_days):
        tasks.append(
            executor.submit(
                _fetch_window,
                client,
                project_id,
                group_by,
                flt,
                name,
                end,
                newer,
                min(newer + chunk_days, days),
            )
        )
    for future in concurrent.futures.as_completed(tasks):
      series, failures = future.result()
      results.extend(series)
      missing.extend(failures)
  return SeriesResult(results, sorted(missing))


def sum_filter(
    client: monitoring_v3.MetricServiceClient,
    project_id: str,
    flt: str,
    end: datetime.datetime,
    days: int,
) -> float:
  """Σ every daily point matching `flt` over the `days` before `end`.

  Args:
    client: Cloud Monitoring client.
    project_id: project to read.
    flt: time series filter.
    end: exclusive end of the window.
    days: window length in days.

  Returns:
    The sum of every matching daily point.

  Raises:
    RuntimeError: if any window could not be read, so a gap is never read as
      zero.
  """
  series, missing = _fetch_window(
      client, project_id, [], flt, "sum", end, 0, days
  )
  if missing:
    raise RuntimeError(f"could not read {', '.join(missing)}")
  total = 0
  for ts in series:
    for _, value in _extract_points(ts):
      total += value
  return float(total)


def query_severity_volume(
    client: monitoring_v3.MetricServiceClient,
    project_id: str,
    top_services: List[str],
    now: datetime.datetime,
    days: int = DEFAULT_SAMPLE_DAYS,
    chunk_days: int = 7,
) -> SeriesResult:
  """Queries `byte_count` per (severity, resource type) for `top_services`."""
  return _fetch_windowed(
      client,
      project_id,
      ['metric.label."severity"', "resource.type"],
      now,
      days,
      chunk_days,
      [(s, f'{_BYTE_COUNT} AND resource.type = "{s}"') for s in top_services],
  )


def query_stream_volume(
    client: monitoring_v3.MetricServiceClient,
    project_id: str,
    now: datetime.datetime,
    days: int = DEFAULT_SAMPLE_DAYS,
    chunk_days: int = 3,
) -> SeriesResult:
  """Queries `byte_count` per (log, severity) across `days`."""
  # Single source for all per-stream `byte_count` reads: summing a day's
  # streams equals the ungrouped total.
  return _fetch_windowed(
      client,
      project_id,
      ["metric.label.log", "metric.label.severity"],
      now,
      days,
      chunk_days,
      [("byte_count", _BYTE_COUNT)],
  )


def _extract_points(ts: Any) -> List[List[Any]]:
  """Extracts daily `[date, value]` points from a GCM TimeSeries."""
  # Points are labelled by the day the bucket covers (end_time minus one day),
  # not the following midnight at which it ends.
  points = []
  for point in ts.points:
    bucket_start = point.interval.end_time - datetime.timedelta(
        seconds=_ALIGNMENT_SECONDS
    )
    value = point.value.int64_value or int(round(point.value.double_value))
    points.append([bucket_start.strftime("%Y-%m-%d"), value])
  return points


def _collapse(parsed: Dict[Any, Dict[str, int]]) -> Dict[Any, List[List[Any]]]:
  """Renders an accumulated `{key: {date: value}}` map as sorted point lists."""
  return {
      key: [[d, dates[d]] for d in sorted(dates)]
      for key, dates in parsed.items()
  }


def parse_stream_results(
    results: List[Any],
) -> Dict[Tuple[str, str], List[List[Any]]]:
  """Parses `byte_count` series into daily history per (log_id, severity)."""
  # Values accumulate because chunked windows return one series per chunk;
  # series without a log label cannot be attributed and are dropped.
  parsed: Dict[Tuple[str, str], Dict[str, int]] = collections.defaultdict(
      lambda: collections.defaultdict(int)
  )
  for ts in results:
    labels = ts.metric.labels
    log_id = labels.get("log", "")
    if not log_id:
      continue
    key = (log_id, labels.get("severity") or DEFAULT_SEVERITY)
    for date_str, val in _extract_points(ts):
      parsed[key][date_str] += val
  return _collapse(parsed)


def parse_severity_results(
    results: List[Any],
) -> Dict[str, Dict[str, List[List[Any]]]]:
  """Parses GCM severity results into daily history per service and severity."""
  parsed: Dict[str, Dict[str, Dict[str, int]]] = collections.defaultdict(
      lambda: collections.defaultdict(lambda: collections.defaultdict(int))
  )
  for ts in results:
    service = ts.resource.type or "unknown"
    severity = ts.metric.labels.get("severity") or DEFAULT_SEVERITY
    for date_str, val in _extract_points(ts):
      parsed[service][severity][date_str] += val
  return {service: _collapse(sevs) for service, sevs in parsed.items()}


def parse_billing_results(results: List[Any]) -> Dict[str, List[List[Any]]]:
  """Parses billed-bytes series into daily history per resource type."""
  # Values accumulate because several series can share a `resource_type`;
  # series without one go under "unknown".
  parsed: Dict[str, Dict[str, int]] = collections.defaultdict(
      lambda: collections.defaultdict(int)
  )
  for ts in results:
    service = ts.metric.labels.get("resource_type") or "unknown"
    for date_str, val in _extract_points(ts):
      parsed[service][date_str] += val
  return _collapse(parsed)
