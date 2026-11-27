"""Collects GCP logging volume and cost data.

Sources: Cloud Monitoring, Log Analytics, and the BigQuery billing export.
"""

import collections
from collections.abc import Sequence
import concurrent.futures
import datetime
import os
from typing import Any, Dict, List, Optional

from absl import app
from absl import flags
from actions import merge_actions
from aggregations import get_daily_services
from aggregations import get_mom_patterns
from aggregations import get_monthly_aggregations
from aggregations import get_severity_summary
from aggregations import get_trailing_30d_summary
from aggregations import get_weekly_aggregations
from aggregations import invoiced_window_gib
from aggregations import latest_complete_month
from aggregations import merge_data
from aggregations import project_month
from aggregations import top_driver
from aggregations import window_sums
from analytics import detect_log_analytics_buckets
from analytics import fetch_logging_api_samples
from analytics import probe_log_analytics_data
from analytics import query_log_analytics_breakdown
import attribution
import billing
from billing import resolve_billing_source
from constants import DEFAULT_ANALYSIS_MONTHS
from constants import DEFAULT_LOCATION
from constants import DEFAULT_SAMPLE_DAYS
from constants import DEFAULT_TELEMETRY_LOOKBACK_DAYS
from constants import MONITORING_RETENTION_DAYS
from constants import write_json
from exclusion_rules import generate_exclusion_candidates
from google.cloud import bigquery
from google.cloud import logging_v2
from google.cloud import monitoring_v3
from google.cloud.logging_v2.services import config_service_v2
from inventory import authed_session
from inventory import fetch_flow_log_configs
from inventory import fetch_log_router_inventory
from inventory import resolve_log_read_scope
from monitoring import get_query_interval
from monitoring import parse_billing_results
from monitoring import parse_severity_results
from monitoring import parse_stream_results
from monitoring import query_log_volume
from monitoring import query_severity_volume
from monitoring import query_stream_volume
from output import print_advisory
from output import write_monthly_details
from output import write_service_details
import perf
from pricing import build_price_book
from provenance import build_provenance
import telemetry_integrity
from waste import compute_extraneous_spend

ConfigServiceV2Client = config_service_v2.ConfigServiceV2Client

FLAGS = flags.FLAGS
if "project-id" not in FLAGS:
  flags.DEFINE_string("project-id", None, "GCP Project ID to query.")
if "output" not in FLAGS:
  flags.DEFINE_string(
      "output",
      "logging_usage_summary.json",
      "Output JSON file path for summary index.",
  )
if "billing-project" not in FLAGS:
  flags.DEFINE_string(
      "billing-project",
      None,
      "Optional GCP Project ID where BigQuery billing export resides.",
  )
if "billing-dataset" not in FLAGS:
  flags.DEFINE_string(
      "billing-dataset",
      None,
      "Optional BigQuery dataset containing billing export tables.",
  )
if "billing-table" not in FLAGS:
  flags.DEFINE_string(
      "billing-table",
      None,
      "Optional explicit BigQuery billing export table name (e.g."
      " `proj.ds.gcp_billing_export_v1_XXXX`).",
  )
if "billing-mode" not in FLAGS:
  flags.DEFINE_enum(
      "billing-mode",
      billing.MODE_SEARCH,
      list(billing.BILLING_MODES),
      "What is already known about where the Cloud Billing BigQuery export"
      " lives. 'explicit' probes only what --billing-table/-project/-dataset"
      " names (~2s, invoiced costs); 'none' skips discovery entirely because"
      " the caller has confirmed there is no export (instant, estimated"
      " costs); 'search' (default) looks for it -- this project first, then"
      " every project on the billing account.",
  )


def collect_data(
    monitoring_client: monitoring_v3.MetricServiceClient,
    project_id: str,
    output_path: str,
    now: datetime.datetime,
    config_client: Optional[ConfigServiceV2Client] = None,
    bq_client: Optional[bigquery.Client] = None,
    sample_days: int = DEFAULT_SAMPLE_DAYS,
    location: str = DEFAULT_LOCATION,
    billing_project: Optional[str] = None,
    billing_dataset: Optional[str] = None,
    billing_table: Optional[str] = None,
    analysis_months: int = DEFAULT_ANALYSIS_MONTHS,
    logging_client: Optional[Any] = None,
    billing_mode: str = billing.MODE_SEARCH,
    http_session: Optional[Any] = None,
) -> Dict[str, Any]:
  """Collects all sources, writes the summary JSON, and returns it."""
  timer = perf.StageTimer()
  client_info = attribution.client_info(attribution.COLLECT_LOGGING_DATA)
  if config_client is None:
    config_client = ConfigServiceV2Client(client_info=client_info)
  if bq_client is None:
    bq_client = bigquery.Client(project=project_id, client_info=client_info)
  if logging_client is None:
    logging_client = logging_v2.Client(
        project=project_id, client_info=client_info
    )
  # Inventory checks that could not run are disclosed, never read as "none".
  inventory_unavailable: List[str] = []
  if http_session is None:
    try:
      http_session = authed_session()
    except Exception as e:  # pylint: disable=broad-except
      print(f"Notice: unable to build an authorized session: {e}")
      inventory_unavailable.append(f"authorized session: {e}")

  def _run_pillar_analytics():
    with timer.stage("log_analytics_buckets"):
      detected_buckets = detect_log_analytics_buckets(
          config_client, project_id, location
      )
    analytics_enabled_buckets = [
        b for b in detected_buckets if b["analytics_enabled"]
    ]
    is_analytics_enabled = len(analytics_enabled_buckets) > 0

    probe_info = {
        "status": "disabled",
        "days_available": 0.0,
        "table_name": None,
    }
    granular_raw = None
    if is_analytics_enabled:
      active = analytics_enabled_buckets[0]
      active_loc = active["location"]
      with timer.stage("log_analytics_probe"):
        probe_info = probe_log_analytics_data(
            bq_client,
            project_id,
            location=active_loc,
            bucket_id=active["bucket_id"],
            sample_days=sample_days,
            now=now,
            linked_dataset=active["linked_dataset"],
        )
      if probe_info["status"] in ("partial_window", "mature"):
        with timer.stage("log_analytics_breakdown"):
          granular_raw = query_log_analytics_breakdown(
              bq_client,
              probe_info["table_name"],
              sample_days=sample_days,
              location=active_loc,
          )
    return detected_buckets, is_analytics_enabled, probe_info, granular_raw

  def _run_pillar_billing():
    return resolve_billing_source(
        bq_client=bq_client,
        project_id=project_id,
        override_table=billing_table,
        billing_project=billing_project,
        billing_dataset=billing_dataset,
        analysis_months=analysis_months,
        now=now,
        billing_mode=billing_mode,
    )

  def _run_billing_chain():
    """Resolves billing, then the billed-volume series whose window needs it."""
    with timer.stage("billing_discovery"):
      billing_result = _run_pillar_billing()
    lookback = (
        MONITORING_RETENTION_DAYS
        if billing_result.invoiced
        else DEFAULT_TELEMETRY_LOOKBACK_DAYS
    )
    with timer.stage("gcm_billed_bytes"):
      results = query_log_volume(
          monitoring_client, project_id, get_query_interval(now, lookback)
      )
    return billing_result, parse_billing_results(results)

  def _run_stream_volume():
    """Fetches `byte_count` once for all consumers."""
    with timer.stage("gcm_byte_count_streams"):
      return query_stream_volume(
          monitoring_client,
          project_id,
          now=now,
          days=int(max(sample_days, DEFAULT_TELEMETRY_LOOKBACK_DAYS)),
      )

  def _run_router_inventory():
    if http_session is None:
      return {"sinks": [], "exclusions": []}, []
    with timer.stage("log_router_inventory"):
      return fetch_log_router_inventory(http_session, project_id)

  def _run_flow_log_configs():
    if http_session is None:
      return [], []
    with timer.stage("flow_log_configs"):
      return fetch_flow_log_configs(http_session, project_id)

  def _run_log_read_scope():
    with timer.stage("log_read_scope"):
      return resolve_log_read_scope(http_session, project_id)

  # These groups are independent, so they run concurrently.
  with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
    fut_analytics = executor.submit(_run_pillar_analytics)
    fut_billing = executor.submit(_run_billing_chain)
    fut_streams = executor.submit(_run_stream_volume)
    fut_router = executor.submit(_run_router_inventory)
    fut_flow_logs = executor.submit(_run_flow_log_configs)
    fut_read_scope = executor.submit(_run_log_read_scope)

    detected_buckets, is_analytics_enabled, probe_info, granular_raw = (
        fut_analytics.result()
    )
    billing_result, parsed_billing = fut_billing.result()
    stream_series = fut_streams.result()
    router_inventory, router_unavailable = fut_router.result()
    flow_log_configs, flow_unavailable = fut_flow_logs.result()
    read_scope = fut_read_scope.result()
  inventory_unavailable += router_unavailable + flow_unavailable

  parsed_streams = parse_stream_results(stream_series.series)
  if stream_series.missing_windows:
    print(
        "Notice: byte_count is incomplete for"
        f" {len(stream_series.missing_windows)} window(s):"
        f" {', '.join(stream_series.missing_windows)}"
    )

  # `billing/bytes_ingested` can silently under-report billed volume. Suspect
  # days are disclosed, never dropped (it is the only per-service split). The
  # invoice is the control when present; else `byte_count` (relative only).
  billed_daily = telemetry_integrity.daily_totals(parsed_billing)
  billing_costs = billing_result.costs or {}
  invoiced_daily_gib = billing_costs.get("daily_gib")
  if invoiced_daily_gib:
    telemetry_verdict = telemetry_integrity.assess_against_invoice(
        billed_daily=billed_daily,
        invoiced_daily_gib=invoiced_daily_gib,
        now=now,
    )
  else:
    # Summing the per-stream series equals the ungrouped daily total.
    telemetry_verdict = telemetry_integrity.assess(
        billed_daily=billed_daily,
        received_daily=telemetry_integrity.daily_totals(parsed_streams),
    )
  if telemetry_verdict["compromised_days"]:
    print(
        "[TELEMETRY INTEGRITY]"
        f" {len(telemetry_verdict['compromised_days'])} day(s) of"
        " billed-volume telemetry under-report the volume that was billed:"
        f" {', '.join(telemetry_verdict['compromised_days'])}"
    )

  billed_by_service = window_sums(parsed_billing, now, sample_days)
  top_services = sorted(
      billed_by_service, key=billed_by_service.get, reverse=True
  )[:5]
  analytics_status = probe_info["status"]
  granular_analytics: Optional[Dict[str, Any]] = None
  severity_missing: List[str] = []

  if analytics_status == "mature":
    parsed_severity = granular_raw["severity_history"]
  else:
    with timer.stage("gcm_severity_volume"):
      severity_series = query_severity_volume(
          monitoring_client, project_id, top_services, now, days=sample_days
      )
    severity_missing = severity_series.missing_windows
    parsed_severity = parse_severity_results(severity_series.series)

  # Extract SQL samples if available, then fetch missing via Logging API
  samples_by_service: Dict[str, Dict[str, List[Dict[str, Any]]]] = (
      collections.defaultdict(lambda: collections.defaultdict(list))
  )
  if granular_raw is not None:
    for srv_name, sevs in granular_raw["samples_by_service"].items():
      for sev_name, items in sevs.items():
        samples_by_service[srv_name][sev_name].extend(items)

  with timer.stage("logging_api_samples"):
    sample_errors = fetch_logging_api_samples(
        logging_client=logging_client,
        project_id=project_id,
        top_services=top_services,
        parsed_severity=parsed_severity,
        samples_by_service=samples_by_service,
        now=now,
        lookback_days=sample_days,
        read_scope=read_scope,
    )
  samples_dict = {srv: dict(sevs) for srv, sevs in samples_by_service.items()}

  merged_data = merge_data(parsed_billing, parsed_severity)
  base_dir = os.path.dirname(os.path.abspath(output_path))
  write_monthly_details(
      parsed_billing, os.path.join(base_dir, "monthly_details"), project_id
  )
  write_service_details(
      merged_data,
      os.path.join(base_dir, "service_details"),
      project_id,
      samples_by_service=samples_dict,
  )

  # The invoice sets the run rate; the metric supplies the service split.
  trailing_30d = get_trailing_30d_summary(
      parsed_billing=parsed_billing,
      now=now,
      invoiced_daily_gib=billing_costs.get("daily_gib"),
  )
  monthly_run_rate_gib = trailing_30d["monthly_run_rate_gib"]

  # Every dollar in the summary is priced from this book: per SKU, with the
  # 50 GiB free tier on Log Storage only.
  stream_sums = window_sums(parsed_streams, now, sample_days)
  price_book = build_price_book(
      baseline_gib=monthly_run_rate_gib,
      now=now,
      window_start=trailing_30d["window_start"],
      monthly_costs=billing_costs.get("monthly_costs"),
      daily_gib_by_sku=billing_costs.get("daily_gib_by_sku"),
      bytes_by_stream=stream_sums,
  )
  trailing_30d["projected_monthly_cost_usd"] = price_book.baseline_cost
  trailing_30d["projected_annual_cost_usd"] = round(
      price_book.baseline_cost * 12.0, 2
  )
  # Price each service on its window GiB scaled to the monthly run rate.
  window_gib = trailing_30d["total_gib"]
  to_monthly = monthly_run_rate_gib / window_gib if window_gib > 0 else 0.0
  for entry in trailing_30d["top_services"]:
    if not entry.get("is_remainder"):
      entry["cost_usd"] = price_book.service_cost(
          entry["service"], entry["gib"] * to_monthly
      )
  trailing_30d["top_driver"] = top_driver(trailing_30d["top_services"])

  monthly_aggs = get_monthly_aggregations(
      billing_data=parsed_billing,
      price_book=price_book,
      billing_costs=billing_costs,
      now=now,
  )
  invoiced_months = sorted(
      m
      for m, entry in monthly_aggs.items()
      if entry["data_source"] == "actual_bq_billing"
  )
  # Named from the months actually retrieved, not the months requested.
  reporting_mode = (
      f"billing_invoiced_{len(invoiced_months)}mo"
      if invoiced_months
      else "telemetry_trailing_30d"
  )

  weekly_aggs = get_weekly_aggregations(
      parsed_billing=parsed_billing, now=now, price_book=price_book
  )
  mom_trends = get_mom_patterns(monthly_aggs)
  cost_projection = project_month(
      now=now,
      price_book=price_book,
      parsed_billing=parsed_billing,
      invoiced_daily_gib_by_sku=billing_costs.get("daily_gib_by_sku"),
  )

  # Present only when the Log Analytics breakdown ran.
  if granular_raw is not None:
    granular_analytics = {
        "sample_period_days": probe_info["days_available"],
        "sample_start": probe_info["earliest_log"],
        "sample_end": probe_info["latest_log"],
        "top_log_names": granular_raw["top_log_names"],
        "top_signatures": granular_raw["top_signatures"],
        # Gross run rate: the book subtracts the free tier itself.
        "exclusion_candidates": generate_exclusion_candidates(
            granular_raw["top_signatures"],
            price_book,
            project_id=project_id,
            total_entries=probe_info["total_entries"],
            total_sample_bytes=granular_raw["total_payload_bytes"],
            monthly_run_rate_gib=monthly_run_rate_gib,
            sample_days=probe_info["days_available"],
        ),
    }

  severity_summary = get_severity_summary(
      parsed_severity,
      now,
      days=sample_days,
      samples_by_service=samples_dict,
      severity_source=(
          "log_analytics"
          if analytics_status == "mature"
          else "cloud_monitoring"
      ),
  )
  # Without this, a truncated fetch looks like a real drop in ERROR volume.
  severity_summary["missing_windows"] = severity_missing
  severity_summary["sample_errors"] = sample_errors

  daily_services = get_daily_services(parsed_billing, now, days=sample_days)

  # Uses Cloud Monitoring volume and router/flow-log inventory, never payload
  # byte sums (which overstate billed volume).
  extraneous_spend, lever_actions = compute_extraneous_spend(
      billed_by_service=billed_by_service,
      byte_count_by_stream=stream_sums,
      window_days=float(sample_days),
      monthly_gib=monthly_run_rate_gib,
      price_book=price_book,
      project_id=project_id,
      sinks=router_inventory["sinks"],
      exclusions=router_inventory["exclusions"],
      buckets=detected_buckets,
      flow_log_configs=flow_log_configs,
      # Invoiced basis, matching the run rate it is divided by.
      billed_window_gib=invoiced_window_gib(
          billing_costs.get("daily_gib"),
          now,
          float(sample_days),
      ),
  )
  extraneous_spend["inventory_unavailable"] = inventory_unavailable

  # Merges levers and exclusion rules on the same stream into one action.
  reduction_actions = merge_actions(
      lever_actions,
      granular_analytics["exclusion_candidates"] if granular_analytics else [],
      price_book,
  )

  index_content = {
      "project_id": project_id,
      "last_updated": now.isoformat(),
      "reporting_mode": reporting_mode,
      "trailing_30d_summary": trailing_30d,
      # How every dollar was priced; read by the report and Prove It.
      "pricing": price_book.to_dict(),
      "weekly_aggregations": weekly_aggs,
      "analytics_metadata": {
          "enabled": is_analytics_enabled,
          "status": analytics_status,
          "days_available": probe_info["days_available"],
          # The `_AllLogs` view the breakdown measured; Prove It queries it.
          "table_name": probe_info["table_name"],
          "buckets": detected_buckets,
          # Where Logging API samples were read; explains empty samples.
          "log_read_scope": read_scope,
      },
      "billing_metadata": billing_result.summary(),
      "monthly_aggregations": monthly_aggs,
      "latest_complete_month": latest_complete_month(monthly_aggs),
      "mom_patterns": mom_trends,
      "cost_projection": cost_projection,
      "severity_summary": severity_summary,
      "daily_services": daily_services,
      "extraneous_spend": extraneous_spend,
      "reduction_actions": reduction_actions,
      "telemetry_integrity": telemetry_verdict,
      # Per-stage timings.
      "collection_profile": timer.profile(),
  }

  if granular_analytics is not None:
    index_content["granular_analytics"] = granular_analytics

  # Built last from the finished summary; source of truth for "Prove It" and
  # `verify_claim.py`.
  index_content["provenance"] = build_provenance(index_content)

  write_json(output_path, index_content)
  print(timer.render())

  print_advisory(index_content, output_path)

  return index_content


def main(argv: Sequence[str]) -> None:
  if len(argv) > 1:
    raise app.UsageError("Too many command-line arguments.")
  project_id = FLAGS["project-id"].value
  if not project_id:
    raise app.UsageError("Flag --project-id is required.")
  if FLAGS["billing-mode"].value == billing.MODE_EXPLICIT and not (
      FLAGS["billing-table"].value
      or FLAGS["billing-project"].value
      or FLAGS["billing-dataset"].value
  ):
    raise app.UsageError(
        "--billing-mode=explicit needs --billing-table, --billing-project or"
        " --billing-dataset."
    )

  # Optional clients are built by `collect_data`.
  collect_data(
      monitoring_client=monitoring_v3.MetricServiceClient(
          client_info=attribution.client_info(attribution.COLLECT_LOGGING_DATA)
      ),
      project_id=project_id,
      output_path=FLAGS["output"].value,
      now=datetime.datetime.now(datetime.timezone.utc),
      billing_project=FLAGS["billing-project"].value,
      billing_dataset=FLAGS["billing-dataset"].value,
      billing_table=FLAGS["billing-table"].value,
      billing_mode=FLAGS["billing-mode"].value,
  )


if __name__ == "__main__":
  app.run(main)
