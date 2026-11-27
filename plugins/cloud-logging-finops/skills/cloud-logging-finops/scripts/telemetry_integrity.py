"""Detects days whose `billing/bytes_ingested` telemetry cannot be believed.

The metric is the only per-service volume source but can silently under-report
a day while its series stays dense and on schedule. Days are checked against
the billing export when available (ratio ~1.0 when healthy), else against
`byte_count` (received bytes; only its ratio stability is informative). This
module only reports; no day is dropped.
"""

import datetime
import statistics
from typing import Any, Dict, List, Mapping, Optional, Sequence

from constants import BYTE_COUNT_METRIC
from constants import BYTES_PER_GIB
from pricing import complete_days

INVOICE_CONTROL = "cloud_billing_bigquery_export"

# --- Invoice control ---------------------------------------------------------

# Healthy days sit near 1.0 of the invoice; failures lose most of the volume.
COMPROMISED_INVOICE_RATIO = 0.5

# Smaller invoiced days are skipped: rounding and the 8h Pacific/UTC day offset
# dominate their ratio.
MIN_INVOICED_GIB = 0.1

# Each day is judged on its own, so fewer days are needed than for `byte_count`.
MIN_DAYS_FOR_INVOICE_VERDICT = 3

# --- `byte_count` fallback control -------------------------------------------

# A day is compromised below this fraction of the window's median ratio.
SUSPECT_RATIO_FRACTION = 0.5

# Below this median the router may drop most logs, or the metric may be broken
# throughout; telemetry alone cannot tell which.
MIN_PLAUSIBLE_MEDIAN_RATIO = 0.15

# Fewer comparable days give no stable median.
MIN_DAYS_FOR_VERDICT = 5

# Near-idle days give ratios dominated by rounding.
MIN_CONTROL_BYTES = 1024 * 1024


def daily_totals(
    parsed: Mapping[Any, Sequence[Sequence[Any]]],
) -> Dict[str, float]:
  """Collapses a `{key: [[date, value], ...]}` series into per-day totals."""
  totals: Dict[str, float] = {}
  for points in parsed.values():
    for day, value in points:
      totals[day] = totals.get(day, 0.0) + value
  return totals


def assess_against_invoice(
    billed_daily: Mapping[str, float],
    invoiced_daily_gib: Mapping[str, float],
    now: datetime.datetime,
) -> Dict[str, Any]:
  """Reports which days of billed telemetry disagree with the invoice.

  Args:
    billed_daily: Per-day bytes from `billing/bytes_ingested`, by UTC day.
    invoiced_daily_gib: Per-day GiB from the billing export, by Pacific day. The
      8h offset is left uncorrected; it cannot cross a 2x threshold.
    now: Current time; invoice days not yet complete are dropped.

  Returns:
    A verdict dict; `status` is `ok`, `degraded` (see `compromised_days`) or
    `unverified` (too few comparable days).
  """
  # Only days the metric also reported are compared, so the metric's own
  # window bounds the overlap.
  ratios = {
      day: billed_daily[day] / (gib * BYTES_PER_GIB)
      for day, gib in complete_days(invoiced_daily_gib, "", now).items()
      if gib >= MIN_INVOICED_GIB and day in billed_daily
  }
  if len(ratios) < MIN_DAYS_FOR_INVOICE_VERDICT:
    return _verdict(
        "unverified",
        INVOICE_CONTROL,
        None,
        len(ratios),
        f"Only {len(ratios)} fully-invoiced day(s) overlap the metric window,"
        " too few to judge whether billing/bytes_ingested reports the volume"
        " that was billed. Service and severity shares are unverified.",
    )

  median_ratio = statistics.median(ratios.values())
  compromised = sorted(
      d for d, r in ratios.items() if r < COMPROMISED_INVOICE_RATIO
  )
  if not compromised:
    return _verdict(
        "ok",
        INVOICE_CONTROL,
        median_ratio,
        len(ratios),
        f"All {len(ratios)} invoiced days in the window are matched by"
        " billing/bytes_ingested.",
    )
  return _verdict(
      "degraded",
      INVOICE_CONTROL,
      median_ratio,
      len(ratios),
      "Cloud Monitoring's billing/bytes_ingested reported under"
      f" {COMPROMISED_INVOICE_RATIO:.0%} of the invoiced volume on"
      f" {len(compromised)} of {len(ratios)} days"
      f" ({_summarise_days(compromised)}). Costs, volumes and run rates come"
      " from the billing export and are unaffected; the service and severity"
      " split on those days is indicative only.",
      compromised,
  )


def _summarise_days(days: Sequence[str]) -> str:
  """Renders a day list compactly; never as a range, as days are scattered."""
  if len(days) <= 4:
    return ", ".join(days)
  return (
      f"{', '.join(days[:3])} and {len(days) - 3} others, most recently"
      f" {days[-1]}"
  )


def assess(
    billed_daily: Mapping[str, float],
    received_daily: Mapping[str, float],
) -> Dict[str, Any]:
  """Reports which days of billed telemetry are too low to be believed.

  Used only without a billing export. `byte_count` is not billed volume, so
  only a day's billed:received ratio relative to the window median is judged.

  Args:
    billed_daily: per-day totals from `billing/bytes_ingested`.
    received_daily: per-day totals from `byte_count`.

  Returns:
    A verdict dict; `status` is `ok`, `degraded` (`compromised_days` far below
    the window median) or `unverified` (no usable control or too few days).
  """
  control = BYTE_COUNT_METRIC
  ratios = {
      day: billed_daily[day] / received
      for day, received in received_daily.items()
      if received >= MIN_CONTROL_BYTES and day in billed_daily
  }
  if len(ratios) < MIN_DAYS_FOR_VERDICT:
    return _verdict(
        "unverified",
        control,
        None,
        len(ratios),
        f"Only {len(ratios)} day(s) could be compared against {control}, too"
        " few to tell an incomplete metric write from a real change in"
        " volume. Figures derived from billing/bytes_ingested are unverified.",
    )

  median_ratio = statistics.median(ratios.values())
  if median_ratio < MIN_PLAUSIBLE_MEDIAN_RATIO:
    return _verdict(
        "unverified",
        control,
        median_ratio,
        len(ratios),
        "Across the window, billing/bytes_ingested reports a median of"
        f" {median_ratio:.1%} of what {control} received. Either the Log"
        " Router drops most of this project's volume, or the billed metric is"
        " incomplete throughout; telemetry alone cannot tell which, so no day"
        " was flagged.",
    )

  threshold = median_ratio * SUSPECT_RATIO_FRACTION
  compromised = sorted(d for d, r in ratios.items() if r < threshold)
  if not compromised:
    return _verdict(
        "ok",
        control,
        median_ratio,
        len(ratios),
        f"All {len(ratios)} comparable days hold a billed:received ratio"
        f" consistent with the window median of {median_ratio:.2f}.",
    )
  return _verdict(
      "degraded",
      control,
      median_ratio,
      len(ratios),
      "billing/bytes_ingested reported under"
      f" {SUSPECT_RATIO_FRACTION:.0%} of its usual share of {control} on"
      f" {len(compromised)} day(s) ({_summarise_days(compromised)}), against"
      f" a window median billed:received ratio of {median_ratio:.2f}. With no"
      " billing export, the comparison is against received rather than"
      " invoiced bytes and cannot rule out a genuine change in what is"
      " billable.",
      compromised,
  )


def _verdict(
    status: str,
    control_metric: str,
    median_ratio: Optional[float],
    days_observed: int,
    note: str,
    compromised: Optional[List[str]] = None,
) -> Dict[str, Any]:
  """Assembles the verdict dict shared by every branch of both assessors."""
  return {
      "status": status,
      "control_metric": control_metric,
      "median_billed_to_received_ratio": (
          None if median_ratio is None else round(median_ratio, 4)
      ),
      "days_observed": days_observed,
      "compromised_days": list(compromised or []),
      "note": note,
  }
