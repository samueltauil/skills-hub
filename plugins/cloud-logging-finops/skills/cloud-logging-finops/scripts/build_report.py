#!/usr/bin/env python3
"""Builds a deterministic, interactive Cloud Logging FinOps HTML report.

Fills `assets/report_template.html` with `logging_usage_summary.json` and an
optional agent-authored `insights/executive_summary.html`. Standard library
only.
"""

import argparse
import datetime
import html
import json
import os
import pathlib
import sys
from typing import Any, Dict, List, Optional, Tuple


def load_summary_data(summary_path: str) -> Dict[str, Any]:
  """Loads the logging usage summary JSON file."""
  with open(summary_path, "r", encoding="utf-8") as f:
    return json.load(f)


def load_template(template_path: Optional[str] = None) -> str:
  """Loads the HTML template from `template_path` or the skill's assets."""
  if template_path:
    candidate_paths = [pathlib.Path(template_path)]
  else:
    # Unresolved __file__ first: runfiles symlinks point at dirs without assets.
    candidate_paths = [
        pathlib.Path(__file__).parent.parent
        / "assets"
        / "report_template.html",
        pathlib.Path(__file__).resolve().parent.parent
        / "assets"
        / "report_template.html",
    ]
  for p in candidate_paths:
    if p.is_file():
      return p.read_text(encoding="utf-8")
  raise FileNotFoundError(
      "report_template.html not found at "
      + ", ".join(str(p) for p in candidate_paths)
  )


def load_executive_summary(insights_dir: Optional[str]) -> Optional[str]:
  """Returns the agent-authored `executive_summary.html`, if present."""
  if not insights_dir:
    return None
  path = os.path.join(insights_dir, "executive_summary.html")
  if not os.path.isfile(path):
    return None
  with open(path, "r", encoding="utf-8") as f:
    return f.read().strip() or None


def _money(value: Optional[float]) -> str:
  """Formats a dollar figure, distinguishing an unmeasured value from zero."""
  return "—" if value is None else f"${value:,.2f}"


def _volume(value: Optional[float]) -> str:
  """Formats a GiB figure, distinguishing an unmeasured value from zero."""
  return "—" if value is None else f"{value:,.1f} GiB"


def _finding(badge: str, badge_class: str, body: str) -> str:
  """Renders one executive-summary finding row."""
  return f"""    <div style="display: flex; gap: 14px; align-items: flex-start; background: var(--bg); border: 1px solid var(--border); border-radius: 8px; padding: 14px;">
      <span class="badge {badge_class}" style="flex-shrink: 0; margin-top: 1px;">{badge}</span>
      <div style="font-size: 13px; line-height: 1.5; color: var(--text);">
        {body}
      </div>
    </div>"""


def _recoverable_spend_finding(summary_data: Dict[str, Any]) -> str:
  """Renders the measured recoverable-spend floor from `extraneous_spend`."""
  waste = summary_data["extraneous_spend"]

  # Never substitute another savings figure for an unmeasured floor.
  if waste["status"] != "ok":
    return _finding(
        "RECOVERABLE SPEND",
        "badge-warning",
        "No recoverable-spend floor could be measured &mdash;"
        f" {html.escape(waste['reason'])} No savings figure is shown in place"
        " of one.",
    )

  headline = waste["headline"]
  counted = sum(
      1 for a in summary_data["reduction_actions"]["actions"] if a["counted"]
  )
  # Without the inventory, "no lever found" could just mean "not checked".
  unchecked = ""
  if waste["inventory_unavailable"]:
    unchecked = (
        " Sink, exclusion and flow-log levers could not be checked (Log Router"
        " or VPC inventory unreadable)."
    )
  usd = headline["monthly_savings_usd"]
  gib = headline["monthly_savings_gib"]
  pct = headline["pct_of_billable_spend"]
  uncounted_pct = waste["uncounted_total_pct"]

  if not counted or not usd:
    body = (
        "No cleanup lever cleared the evidence bar for counted savings, so the"
        " recoverable floor for this project is not quantified."
    )
    if uncounted_pct > 0:
      body += (
          ' Levers worth <strong style="color: #c084fc;">'
          f"{uncounted_pct:.1f}%</strong> of billable spend were found but"
          " require owner or compliance judgement, so they are surfaced in the"
          " <em>Extraneous Log Spend</em> card above rather than counted."
      )
    return _finding("RECOVERABLE SPEND", "badge-primary", body + unchecked)

  body = (
      'At least <strong style="color: #34d399;">'
      f"{pct:.1f}% of billable spend</strong> is recoverable &mdash;"
      f' <strong style="color: #34d399;">{_money(usd)}/mo</strong>'
      f" ({_volume(gib)}/mo) across {counted} measured"
      f" lever{'s' if counted != 1 else ''}. This is a floor, not an estimate:"
      " it counts only levers measured against billing metrics whose cleanup"
      " preserves a signal this project has shown it wants. Per-lever evidence"
      " is in the <em>Extraneous Log Spend</em> card above."
  )
  if uncounted_pct > 0:
    body += (
        f' A further <strong style="color: #c084fc;">{uncounted_pct:.1f}%'
        "</strong> sits in levers that need owner or compliance judgement"
        " and is deliberately excluded from this figure."
    )
  if headline["exceeds_sanity_ceiling"]:
    body += (
        ' <strong style="color: #fbbf24;">Flagged for manual review:</strong>'
        " this share is high enough that the underlying measurement should be"
        " confirmed before it is acted on."
    )
  return _finding("RECOVERABLE SPEND", "badge-success", body + unchecked)


def _generate_default_executive_summary(summary_data: Dict[str, Any]) -> str:
  """Generates a default FinOps executive summary card from summary data."""
  is_invoiced = summary_data["billing_metadata"]["invoiced"]

  # Only whole months are comparable.
  monthly_aggs = summary_data["monthly_aggregations"]
  complete = sorted(m for m, d in monthly_aggs.items() if not d["is_partial"])
  if len(complete) >= 2:
    first, last = monthly_aggs[complete[0]], monthly_aggs[complete[-1]]
    span_html = (
        f"Complete billing months {complete[0]} through {complete[-1]} moved"
        f' from <strong style="color: var(--text);">'
        f'{_money(first["net_cost_usd"])}'
        f' ({_volume(first["total_gib"])})</strong> to'
        f' <strong style="color: #fbbf24;">{_money(last["net_cost_usd"])}'
        f' ({_volume(last["total_gib"])})</strong>.'
    )
  elif complete:
    only = monthly_aggs[complete[0]]
    span_html = (
        f"One complete billing month is available ({complete[0]}):"
        f' <strong style="color: var(--text);">'
        f'{_money(only["net_cost_usd"])}'
        f' ({_volume(only["total_gib"])})</strong>.'
    )
  else:
    span_html = (
        "No complete billing month has been observed yet, so no"
        " month-over-month comparison is shown."
    )

  trailing_30d = summary_data["trailing_30d_summary"]
  # Label by days actually observed (may be < 30) and by their source.
  days_observed = trailing_30d["days_observed"]
  invoiced = trailing_30d["volume_basis"] == "invoiced_daily_usage"
  day_word = "invoiced day" if invoiced else "measured day"
  window_label = (
      f"the last {days_observed} {day_word}{'s' if days_observed != 1 else ''}"
      if days_observed
      else "the trailing window"
  )
  span_html += (
      f" Ingestion over {window_label} is"
      ' <strong style="color: var(--text);">'
      f'{_volume(trailing_30d["total_gib"])}</strong>, a projected run rate'
      ' of <strong style="color: #fbbf24;">'
      f'{_money(trailing_30d["projected_monthly_cost_usd"])}/mo'
      f' ({_volume(trailing_30d["monthly_run_rate_gib"])}/mo)</strong>.'
  )

  if is_invoiced:
    months = sum(
        1
        for d in monthly_aggs.values()
        if d["data_source"] == "actual_bq_billing"
    )
    pricing_note = (
        "Actual invoiced BigQuery billing export data, reconciled across"
        f" {months} billing month{'s' if months != 1 else ''}."
    )
  else:
    pricing_note = (
        "Estimated from per-SKU list prices; no billing export was read."
    )
  span_html += (
      '<div style="font-size: 12px; color: var(--text-muted); margin-top:'
      f' 4px;">Note: {html.escape(pricing_note)}</div>'
  )

  findings = [_finding("SPEND &amp; INGESTION", "badge-warning", span_html)]

  # State the measured combined share rather than a qualitative claim.
  named = [
      s for s in trailing_30d["top_services"][:3] if not s.get("is_remainder")
  ]
  if named:
    listed = ", ".join(
        f'<code class="code-pill">{html.escape(s["service"])}</code>'
        f' (<strong style="color: #60a5fa;">{s["pct_of_total"]:.1f}%'
        "</strong>)"
        for s in named
    )
    combined = sum(s["pct_of_total"] for s in named)
    findings.append(
        _finding(
            "PRIMARY DRIVERS",
            "badge-primary",
            f"Ingestion is led by {listed} &mdash;"
            f' <strong style="color: #60a5fa;">{combined:.1f}%</strong> of'
            f" volume over {window_label} between them.",
        )
    )

  # Only the measured floor is stated; action savings overlap and don't sum.
  findings.append(_recoverable_spend_finding(summary_data))

  findings_html = "\n\n".join(findings)
  return f"""<div class="card" style="gap: 16px;">
  <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 12px;">
    <h2 class="section-title">Executive Summary &amp; Key Findings</h2>
    <span class="badge badge-primary">FinOps Assessment</span>
  </div>

  <div style="display: flex; flex-direction: column; gap: 12px;">
{findings_html}
  </div>
</div>"""


# The summary fields report_template.html reads: a top-level key maps to None
# (embed the whole block) or to the only sub-keys the page reads. Everything
# else stays on disk for the agent, so new fields never leak into the page.
PAGE_FIELDS: Dict[str, Optional[Tuple[str, ...]]] = {
    "analytics_metadata": ("status",),
    "billing_metadata": None,
    "cost_projection": None,
    "daily_services": None,
    "extraneous_spend": None,
    "latest_complete_month": None,
    "monthly_aggregations": None,
    "pricing": None,
    "provenance": None,
    "reduction_actions": None,
    "severity_summary": None,
    "telemetry_integrity": None,
    "trailing_30d_summary": None,
    "weekly_aggregations": None,
}


def _browser_payload(summary_data: Dict[str, Any]) -> Dict[str, Any]:
  """Returns the `PAGE_FIELDS` subset of the summary, without claim ledgers."""
  payload: Dict[str, Any] = {}
  for key, sub_keys in PAGE_FIELDS.items():
    value = summary_data[key]
    payload[key] = (
        value if sub_keys is None else {k: value[k] for k in sub_keys}
    )
  # Per-stream claim ledgers are for Prove It and the agent, not the page.
  payload["reduction_actions"] = {
      **payload["reduction_actions"],
      "actions": [
          {k: v for k, v in a.items() if k != "claims"}
          for a in payload["reduction_actions"]["actions"]
      ],
  }
  return payload


def populate_template(
    template_content: str,
    summary_data: Dict[str, Any],
    executive_summary: Optional[str] = None,
    report_context: Optional[Dict[str, str]] = None,
) -> str:
  """Renders the HTML report.

  Args:
    template_content: The report_template.html text.
    summary_data: Parsed logging_usage_summary.json.
    executive_summary: Agent-authored executive summary HTML; a default one is
      generated from the summary when absent.
    report_context: Where the summary, `verify_claim.py` and the Python that can
      run it live on disk, so the Prove It drawer can print a ready-to-run
      re-check command.

  Returns:
    The rendered HTML.
  """
  snapshot_time = datetime.datetime.fromisoformat(
      summary_data["last_updated"]
  ).strftime("%Y-%m-%d %H:%M:%S UTC")

  payload = _browser_payload(summary_data)
  if report_context:
    payload["report_context"] = dict(report_context)
  # Escaped so a string in the data cannot close the <script> element.
  json_data_str = json.dumps(payload, separators=(",", ":")).replace(
      "</", "<\\/"
  )

  rendered = template_content
  rendered = rendered.replace(
      "{{PROJECT_ID}}", html.escape(summary_data["project_id"])
  )
  rendered = rendered.replace("{{SNAPSHOT_TIME}}", snapshot_time)
  rendered = rendered.replace("{{FINOPS_JSON_DATA}}", json_data_str)
  return rendered.replace(
      "<!-- SLOT:EXECUTIVE_SUMMARY -->",
      executive_summary or _generate_default_executive_summary(summary_data),
  )


def compose_report(
    summary_path: str,
    output_path: str,
    insights_dir: Optional[str] = None,
    template_path: Optional[str] = None,
) -> str:
  """Loads the summary and template, renders the report and writes it."""
  summary_data = load_summary_data(summary_path)
  template_content = load_template(template_path)
  html_output = populate_template(
      template_content,
      summary_data,
      load_executive_summary(insights_dir),
      report_context={
          "summary_path": os.path.abspath(summary_path),
          "verify_script": os.path.join(
              os.path.dirname(os.path.abspath(__file__)), "verify_claim.py"
          ),
          # This interpreter has the google-cloud-* deps verify_claim needs.
          "python": sys.executable,
      },
  )

  out_dir = os.path.dirname(output_path)
  if out_dir:
    os.makedirs(out_dir, exist_ok=True)

  with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_output)

  return output_path


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
  """Parses command-line arguments."""
  parser = argparse.ArgumentParser(
      description=(
          "Deterministically build a Cloud Logging FinOps HTML report from"
          " the collector's summary JSON."
      )
  )
  parser.add_argument(
      "--summary",
      "-s",
      default="logging_usage_summary.json",
      help=(
          "Path to logging_usage_summary.json (default:"
          " logging_usage_summary.json)"
      ),
  )
  parser.add_argument(
      "--insights-dir",
      "-i",
      default="insights",
      help=(
          "Directory holding an agent-authored executive_summary.html"
          " (default: insights)"
      ),
  )
  parser.add_argument(
      "--output",
      "-o",
      default="log_usage_report.html",
      help=(
          "Output path for compiled HTML report (default:"
          " log_usage_report.html)"
      ),
  )
  parser.add_argument(
      "--template",
      "-t",
      default=None,
      help="Path to custom report_template.html (optional)",
  )
  return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> None:
  args = parse_args(argv)
  try:
    out_file = compose_report(
        summary_path=args.summary,
        output_path=args.output,
        insights_dir=args.insights_dir,
        template_path=args.template,
    )
    print(f"Successfully generated FinOps report: {out_file}")
  except (OSError, ValueError, KeyError) as e:
    print(f"Error generating FinOps report: {e}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
  main()
