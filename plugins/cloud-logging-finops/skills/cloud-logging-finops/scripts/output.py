"""Partitioned File Exporters and Console Advisories."""

import collections
import os
from typing import Any, Dict, List, Optional

from constants import write_json


def write_monthly_details(
    billing_data: Dict[str, List[List[Any]]],
    output_dir: str,
    project_id: str,
) -> Dict[str, str]:
  """Writes daily history grouped by month into partitioned JSON files."""
  monthly_daily: Dict[str, Dict[str, List[Any]]] = collections.defaultdict(
      lambda: collections.defaultdict(list)
  )
  for service, points in billing_data.items():
    for date_str, val in points:
      monthly_daily[date_str[:7]][service].append(
          [date_str, {"billing_total": val}]
      )

  written_files = {}
  for month, services in monthly_daily.items():
    for srv in services:
      services[srv].sort(key=lambda x: x[0])

    file_name = f"{month}.json"
    write_json(
        os.path.join(output_dir, file_name),
        {"project_id": project_id, "month": month, "services": dict(services)},
    )
    written_files[month] = os.path.join("monthly_details", file_name)

  return written_files


def write_service_details(
    merged_data: Dict[str, Dict[str, Dict[str, Any]]],
    output_dir: str,
    project_id: str,
    samples_by_service: Optional[
        Dict[str, Dict[str, List[Dict[str, Any]]]]
    ] = None,
) -> Dict[str, str]:
  """Writes daily history grouped by service into partitioned JSON files."""
  written_files = {}
  for service, dates in merged_data.items():
    safe_name = service.replace("/", "_")
    file_name = f"{safe_name}.json"
    service_content: Dict[str, Any] = {
        "project_id": project_id,
        "service": service,
        "daily_history": [[d, dates[d]] for d in sorted(dates.keys())],
    }
    if samples_by_service and service in samples_by_service:
      service_content["samples_by_severity"] = samples_by_service[service]
    write_json(
        os.path.join(output_dir, file_name),
        service_content,
    )
    written_files[service] = os.path.join("service_details", file_name)

  return written_files


def _print_billing_advisory(billing: Dict[str, Any]) -> None:
  """Says what the cost figures rest on and how discovery got there."""
  print(
      f"  BigQuery Billing Sync status: {billing['status']} (days available:"
      f" {billing['days_available']:.1f})"
  )
  for step in billing["fallback_chain"]:
    table = f" ({step['table']})" if step.get("table") else ""
    print(f"    - {step['tier']}: {step['status']}{table} - {step['detail']}")

  if not billing["invoiced"]:
    print(
        "\n[FINOPS ADVISORY - BILLING SYNC] No billing export was read, so"
        " costs are list-price estimates from Cloud Monitoring volume."
    )
    print(
        "  - Action for Agent: Tell the user, in plain language, what the"
        " discovery steps above checked and found (SKILL.md Step 3A), that list"
        " pricing was applied, and that --billing-table or"
        " --billing-project/--billing-dataset points at an export elsewhere."
    )
  elif billing["status"] == "partial_window":
    print(
        "\n[FINOPS ADVISORY - BILLING SYNC] BigQuery Billing Export has"
        f" {billing['days_available']:.1f} days of data (active since"
        f" {billing['earliest_date']})."
    )
    print(
        "  - Action for Agent: Hybrid cost analysis used. Invoiced BQ billing"
        " data used for available months; earlier months estimated from usage"
        " volume. Explicitly note this date demarcation in final reports."
    )
  else:
    print(
        "\n[FINOPS ADVISORY - BILLING SYNC] The billing export covers the whole"
        " analysis window. Monthly totals are invoice-accurate, including"
        " credits; service and severity splits are priced before credits."
    )


def print_advisory(summary: Dict[str, Any], output_path: str) -> None:
  """Prints formatted FinOps advisories for the agent and user."""
  analytics = summary["analytics_metadata"]
  status = analytics["status"]
  days_available = analytics["days_available"]
  flow = {
      "mature": "log_analytics",
      "partial_window": "complementary_sample",
  }.get(status, "cloud_monitoring_baseline")
  print("\n[DATA COLLECTION COMPLETE]")
  print(f"  Summary saved to: {output_path}")
  print(f"  Log Analytics status: {status} (flow: {flow})")
  _print_billing_advisory(summary["billing_metadata"])

  if not analytics["enabled"]:
    print(
        "\n[FINOPS ADVISORY - LOG ANALYTICS] Log Analytics is DISABLED on"
        " bucket '_Default'."
    )
    print(
        "  - Action for Agent: Inform the user and recommend enabling Log"
        " Analytics (no extra storage cost; unlocks granular log_name &"
        " container exclusion filters). The upgrade cannot be undone, so end"
        " your reply by asking: \"Do you want me to upgrade the '_Default'"
        " bucket to Log Analytics? This can't be undone.\" Then wait; never"
        " run it in the same turn."
    )
    print("  - Command to enable upon user approval:")
    print(
        "      /tmp/finops_venv/bin/python scripts/enable_log_analytics.py"
        f" --project-id {summary['project_id']}"
    )
  elif status == "too_fresh":
    print(
        "\n[FINOPS ADVISORY - LOG ANALYTICS] Log Analytics was enabled < 24h"
        " ago."
    )
    print(
        "  - Action for Agent: Used 14-day Cloud Monitoring baseline. SQL"
        " breakdowns will unlock as logs accumulate (~1-2 hrs for initial"
        " sample)."
    )
  elif status == "partial_window":
    print(
        "\n[FINOPS ADVISORY - LOG ANALYTICS] Log Analytics has"
        f" {days_available:.1f} days of indexed data."
    )
    print(
        "  - Action for Agent: Stratified flow used (14-day macro severity"
        f" from GCM + {days_available:.1f}-day fine-grained sample). Note this"
        " sample window in reports."
    )
  else:
    print(
        "\n[FINOPS ADVISORY - LOG ANALYTICS] Full Log Analytics data available"
        " (>= 14 days). All breakdowns powered by SQL analytics."
    )
