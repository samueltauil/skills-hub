"""Cost apportionment and volume/cost aggregations over the collected series."""

import calendar
import collections
import datetime
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from constants import BYTES_PER_GIB
from constants import DAYS_PER_MONTH
from constants import DEFAULT_SAMPLE_DAYS
from constants import DEFAULT_TELEMETRY_LOOKBACK_DAYS
from constants import ESTIMATED_SKU_NAME
from pricing import complete_days
from pricing import PriceBook
from pricing import sku_of_resource


def window_start(now: datetime.datetime, days: float) -> str:
  """First date (`YYYY-MM-DD`) of the `days`-day window ending at `now`."""
  return (now - datetime.timedelta(days=days)).strftime("%Y-%m-%d")


def window_sums(
    parsed: Mapping[Any, Sequence[Sequence[Any]]],
    now: datetime.datetime,
    days: float,
) -> Dict[Any, float]:
  """Totals each `[[date, value], ...]` series from `window_start(now, days)`.

  Series are whole UTC days ending before today, so this covers exactly `days`
  days. A series with nothing in the window is omitted rather than reported as
  zero, which would read as a stream that stopped.

  Args:
    parsed: `[[date, value], ...]` series by key.
    now: end of the window.
    days: window length in days.

  Returns:
    The window total per key.
  """
  start = window_start(now, days)
  sums: Dict[Any, float] = {}
  for key, points in parsed.items():
    total = sum(value for day, value in points if day >= start)
    if total:
      sums[key] = total
  return sums


def apportion_cents_exactly(
    weights: Dict[str, int], total_cents: int
) -> Dict[str, float]:
  """Splits integer cents by weight (largest remainder); sum is exact."""
  total_weight = sum(weights.values())
  if total_weight <= 0 or total_cents <= 0:
    return {k: 0.0 for k in weights}

  exact_cents = {
      k: (w * total_cents) / total_weight for k, w in weights.items()
  }
  floor_cents = {k: int(cents) for k, cents in exact_cents.items()}

  remainder_cents = total_cents - sum(floor_cents.values())
  remainders = {k: exact_cents[k] - floor_cents[k] for k in weights}

  for key, _ in sorted(remainders.items(), key=lambda x: x[1], reverse=True)[
      :remainder_cents
  ]:
    floor_cents[key] += 1

  return {k: round(cents / 100.0, 2) for k, cents in floor_cents.items()}


def _apportion_by_sku(
    services_bytes: Dict[str, int],
    total_cents: int,
    ingestion_by_sku: Optional[Dict[str, Dict[str, float]]],
) -> Tuple[Dict[str, float], bool]:
  """Apportions a month's ingestion cost to services, one SKU pool at a time."""
  # Falls back to one pool when fewer than two SKUs carry cost or a priced SKU
  # has no mapped service. Returns (dollars per service summing exactly to
  # `total_cents / 100`, whether the split was per SKU).
  pools: Dict[str, Dict[str, int]] = collections.defaultdict(dict)
  for name, num_bytes in services_bytes.items():
    pools[sku_of_resource(name)][name] = num_bytes
  sku_costs = {
      k: v["net_cost_usd"] for k, v in (ingestion_by_sku or {}).items()
  }
  priced = {k: c for k, c in sku_costs.items() if c > 0}
  if len(priced) < 2 or any(not pools.get(k) for k in priced):
    return apportion_cents_exactly(services_bytes, total_cents), False

  # Whole cents per SKU, closing on the month total by largest remainder.
  sku_cents = {
      k: int(round(v * 100))
      for k, v in apportion_cents_exactly(
          {k: int(round(c * 100)) for k, c in priced.items()}, total_cents
      ).items()
  }
  result: Dict[str, float] = {name: 0.0 for name in services_bytes}
  for sku, cents in sku_cents.items():
    result.update(apportion_cents_exactly(pools[sku], cents))
  return result, True


# ==============================================================================
# Data Merging & Transformation Engine
# ==============================================================================


def merge_data(
    billing_data: Dict[str, List[List[Any]]],
    severity_data: Dict[str, Dict[str, List[List[Any]]]],
) -> Dict[str, Dict[str, Dict[str, Any]]]:
  """Merges billing and severity daily history per service and date."""
  merged: Dict[str, Dict[str, Dict[str, Any]]] = collections.defaultdict(
      lambda: collections.defaultdict(
          lambda: {"billing_total": 0, "severity": {}}
      )
  )

  for service, points in billing_data.items():
    for date_str, val in points:
      merged[service][date_str]["billing_total"] = val

  for service, sevs in severity_data.items():
    for severity, points in sevs.items():
      for date_str, val in points:
        merged[service][date_str]["severity"][severity] = val

  return {
      service: {d: data for d, data in dates.items()}
      for service, dates in merged.items()
  }


def _month_span(month: str) -> int:
  """Returns the number of days in `month` ('YYYY-MM')."""
  return calendar.monthrange(int(month[:4]), int(month[5:7]))[1]


def get_monthly_aggregations(
    billing_data: Dict[str, List[List[Any]]],
    price_book: PriceBook,
    billing_costs: Optional[Dict[str, Any]] = None,
    now: Optional[datetime.datetime] = None,
) -> Dict[str, Dict[str, Any]]:
  """Calculates monthly usage and cost summaries reconciled to the penny.

  Months are the union of telemetry months (42-day Cloud Monitoring retention)
  and invoiced months.

  Args:
    billing_data: Daily `[date, bytes]` points keyed by service.
    price_book: Prices the months the invoice does not cover.
    billing_costs: Optional output of `billing.query_logging_billing_costs`.
    now: Reference instant used to identify the in-progress month.

  Returns:
    A dict keyed by `YYYY-MM` with volume, cost, per-service breakdown and
    partial-month flags.
  """
  telemetry: Dict[str, Dict[str, Any]] = {}
  for service, points in billing_data.items():
    for date_str, val in points:
      month_str = date_str[:7]
      entry = telemetry.setdefault(
          month_str,
          {
              "bytes": 0,
              "services": collections.defaultdict(int),
              "dates": set(),
          },
      )
      entry["services"][service] += val
      entry["bytes"] += val
      entry["dates"].add(date_str)

  b_costs = billing_costs.get("monthly_costs", {}) if billing_costs else {}
  current_month = now.strftime("%Y-%m") if now else None
  monthly: Dict[str, Dict[str, Any]] = {}

  for month in sorted(set(telemetry) | set(b_costs)):
    tele = telemetry.get(month, {})
    services_bytes = dict(
        sorted(
            tele.get("services", {}).items(),
            key=lambda item: item[1],
            reverse=True,
        )
    )
    telemetry_bytes = tele.get("bytes", 0)
    coverage_days = len(tele.get("dates", set()))
    days_in_month = _month_span(month)
    billed = b_costs.get(month)

    if billed:
      raw_cost = billed["raw_cost_usd"]
      credits_amount = billed["credits_usd"]
      net_cost = billed["net_cost_usd"]
      sku_breakdown = billed["sku_breakdown"]
      data_source = "actual_bq_billing"
      total_gib = billed["ingestion_gib"]
      ingestion_cost = billed["ingestion_net_cost_usd"]
      observed_days = billed["billed_days"]
    else:
      total_gib = round(telemetry_bytes / BYTES_PER_GIB, 2)
      gib_by_sku: Dict[str, float] = collections.defaultdict(float)
      for name, num_bytes in services_bytes.items():
        gib_by_sku[price_book.sku_for_resource(name)] += (
            num_bytes / BYTES_PER_GIB
        )
      ingestion_cost = price_book.month_cost(gib_by_sku)
      raw_cost = ingestion_cost
      credits_amount = 0.0
      net_cost = ingestion_cost
      sku_breakdown = {ESTIMATED_SKU_NAME: ingestion_cost}
      data_source = "usage_estimated"
      observed_days = coverage_days

    # A month is partial until it has both ended and been fully observed.
    if month == current_month:
      is_partial, partial_reason = True, "month still in progress"
    elif observed_days < days_in_month:
      is_partial = True
      partial_reason = (
          f"{observed_days} of {days_in_month} days observed"
          f" ({'billing export' if billed else 'Cloud Monitoring retention'})"
      )
    else:
      is_partial, partial_reason = False, None

    # Shares are against the telemetry total, which may cover fewer days than
    # the invoiced total.
    services_basis_bytes = telemetry_bytes
    total_ingest_cents = int(round(ingestion_cost * 100))
    apportioned, services_per_sku = _apportion_by_sku(
        services_bytes,
        total_ingest_cents,
        billed["ingestion_by_sku"] if billed else None,
    )

    services_details: Dict[str, Dict[str, Any]] = {}
    for s_name, s_bytes in services_bytes.items():
      s_cost = apportioned.get(s_name, 0.0)
      share = (
          s_bytes / services_basis_bytes if services_basis_bytes > 0 else 0.0
      )
      services_details[s_name] = {
          "bytes": s_bytes,
          "gib": round(s_bytes / BYTES_PER_GIB, 2),
          "cost_usd": s_cost,
          "pct_of_volume": round(share * 100.0, 1),
      }
      # Telemetry keeps only 42 days; `billed_gib` restates the share on the
      # invoiced month's basis, matching `cost_usd`.
      if billed:
        services_details[s_name]["billed_gib"] = round(share * total_gib, 2)

    monthly[month] = {
        "total_gib": total_gib,
        "raw_cost_usd": raw_cost,
        "credits_usd": credits_amount,
        "net_cost_usd": net_cost,
        "ingestion_cost_usd": ingestion_cost,
        "data_source": data_source,
        "coverage_days": observed_days,
        "is_partial": is_partial,
        "partial_reason": partial_reason,
        "cost_by_sku": sku_breakdown,
        # Ingestion GiB and cost per billing SKU (log_storage / vended), the
        # pools the per-service dollars below are apportioned from.
        "ingestion_by_sku": billed["ingestion_by_sku"] if billed else {},
        "services_cost_basis": "per_sku" if services_per_sku else "blended",
        "services": services_bytes,
        "services_details": services_details,
        "top_service": top_driver(
            [{"service": k, **v} for k, v in services_details.items()]
        ),
        # Days the per-service split was measured over (vs invoiced days).
        "services_telemetry_days": coverage_days,
    }

  return monthly


def get_severity_summary(
    severity_data: Dict[str, Dict[str, List[List[Any]]]],
    now: datetime.datetime,
    days: int = DEFAULT_SAMPLE_DAYS,
    samples_by_service: Optional[
        Dict[str, Dict[str, List[Dict[str, Any]]]]
    ] = None,
    severity_source: str = "cloud_monitoring",
) -> Dict[str, Any]:
  """Summarises severity volume for the last N days.

  Args:
    severity_data: Daily `[date, bytes]` points keyed by service then severity.
    now: Reference instant; the window is the `days` before it.
    days: Length of the summarised window, in days.
    samples_by_service: Optional sampled log patterns keyed by service then
      severity, passed through to the result.
    severity_source: Which measurement the volumes came from, either
      "cloud_monitoring" or "log_analytics".

  Returns:
    A dict with the per-severity totals, the window description, per-service
    and per-day severity breakdowns, and the samples with their coverage.
  """
  start_date_str = window_start(now, days)

  severity_totals: Dict[str, int] = collections.defaultdict(int)
  severity_by_service: Dict[str, Dict[str, int]] = collections.defaultdict(
      lambda: collections.defaultdict(int)
  )
  daily_severity: Dict[str, Dict[str, int]] = collections.defaultdict(
      lambda: collections.defaultdict(int)
  )

  for service, sevs in severity_data.items():
    for sev, points in sevs.items():
      for date_str, val in points:
        if date_str >= start_date_str:
          severity_totals[sev] += val
          severity_by_service[service][sev] += val
          daily_severity[date_str][sev] += val

  def by_value(mapping: Dict[str, int]) -> Dict[str, int]:
    return dict(sorted(mapping.items(), key=lambda x: x[1], reverse=True))

  sorted_totals = by_value(severity_totals)
  sorted_services = sorted(
      severity_by_service,
      key=lambda s: sum(severity_by_service[s].values()),
      reverse=True,
  )

  return {
      "severity_totals": sorted_totals,
      "severity_source": severity_source,
      "window_days": days,
      "severity_by_service": {
          s: by_value(severity_by_service[s]) for s in sorted_services
      },
      "daily_severity": {
          d: by_value(daily_severity[d]) for d in sorted(daily_severity)
      },
      "samples_by_service": samples_by_service or {},
      "sample_coverage": _compute_sample_coverage(
          samples_by_service, severity_by_service, severity_source
      ),
  }


def _compute_sample_coverage(
    samples_by_service: Optional[Dict[str, Dict[str, List[Dict[str, Any]]]]],
    severity_by_service: Dict[str, Dict[str, int]],
    severity_source: str = "cloud_monitoring",
) -> Dict[str, Dict[str, Dict[str, Any]]]:
  """Reports what share of each stream the displayed patterns account for."""
  # The share is withheld unless both sides come from Log Analytics; otherwise
  # stream totals are Cloud Monitoring `byte_count` over a different window.
  coverage: Dict[str, Dict[str, Dict[str, Any]]] = {}
  if not samples_by_service:
    return coverage

  comparable = severity_source == "log_analytics"

  for service, sevs in samples_by_service.items():
    for severity, cards in (sevs or {}).items():
      measured = [c for c in cards if c["volume_measured"]]
      shown_bytes = sum(c["total_bytes"] for c in measured)
      stream_bytes = severity_by_service.get(service, {}).get(severity, 0)

      # Shown and stream totals come from different queries; withhold the share
      # (with a reason) rather than report coverage above 100%.
      if not comparable:
        reason = "bases_differ"
      elif stream_bytes <= 0:
        reason = "stream_volume_not_measured"
      elif shown_bytes > stream_bytes:
        reason = "shown_exceeds_stream"
      else:
        reason = None

      coverage.setdefault(service, {})[severity] = {
          "patterns_shown": len(measured),
          "shown_bytes": shown_bytes,
          "stream_bytes": stream_bytes,
          "shown_pct": (
              None if reason else round(shown_bytes / stream_bytes * 100.0, 1)
          ),
          "remainder_bytes": None if reason else stream_bytes - shown_bytes,
          "shown_pct_withheld": reason,
      }

  return coverage


def invoiced_window_gib(
    invoiced_daily_gib: Optional[Dict[str, float]],
    now: datetime.datetime,
    window_days: float,
) -> Optional[float]:
  """Returns the mean complete invoiced day scaled onto `window_days`."""
  # Metric buckets anchor to `now` and invoice buckets to Pacific days, so only
  # the span is matched. None means no invoiced anchor, not zero volume.
  if window_days <= 0:
    return None
  complete = complete_days(
      invoiced_daily_gib, window_start(now, window_days), now
  )
  if not complete:
    return None
  return (sum(complete.values()) / len(complete)) * window_days


def get_trailing_30d_summary(
    parsed_billing: Dict[str, List[List[Any]]],
    now: datetime.datetime,
    invoiced_daily_gib: Optional[Dict[str, float]] = None,
) -> Dict[str, Any]:
  """Calculates trailing 30-day volume, daily average and monthly run rate."""
  # Volume only; the caller prices it from the price book. Volume comes from
  # the invoice when `invoiced_daily_gib` is supplied, since
  # `billing/bytes_ingested` can silently under-report; the metric is then used
  # only for the per-service split.
  days = DEFAULT_TELEMETRY_LOOKBACK_DAYS
  cutoff_str = window_start(now, days)
  service_bytes = window_sums(parsed_billing, now, days)
  total_bytes = sum(service_bytes.values())
  invoiced = complete_days(invoiced_daily_gib, cutoff_str, now)

  if invoiced:
    total_gib = sum(invoiced.values())
    valid_days = len(invoiced)
    basis = "invoiced_daily_usage"
  else:
    total_gib = total_bytes / BYTES_PER_GIB
    observed_days = set()
    for points in parsed_billing.values():
      for day, _ in points:
        if day >= cutoff_str:
          observed_days.add(day)
    valid_days = max(1, len(observed_days))
    basis = "cloud_monitoring_metric"

  daily_avg_gib = total_gib / valid_days
  monthly_run_rate_gib = daily_avg_gib * DAYS_PER_MONTH

  ranked = sorted(service_bytes.items(), key=lambda kv: kv[1], reverse=True)

  def as_entry(name: str, num_bytes: int) -> Dict[str, Any]:
    # Share from the metric, magnitude from `total_gib`, so services sum to the
    # headline total.
    share = (num_bytes / total_bytes) if total_bytes else 0.0
    return {
        "service": name,
        "gib": round(share * total_gib, 2),
        "pct_of_total": round(share * 100.0, 1),
    }

  top_services = [as_entry(s, b) for s, b in ranked[:5]]
  # Remainder row so the listed shares sum to 100%.
  remainder = sum(b for _, b in ranked[5:])
  if remainder > 0:
    other = as_entry(f"Other ({len(ranked) - 5} services)", remainder)
    # Flagged so consumers need not match on the display name. It mixes
    # services on both SKUs, so it is never priced or ranked as one service.
    other["is_remainder"] = True
    top_services.append(other)

  return {
      "window_start": cutoff_str,
      "days_observed": valid_days,
      "total_gib": round(total_gib, 2),
      "daily_avg_gib": round(daily_avg_gib, 2),
      "monthly_run_rate_gib": round(monthly_run_rate_gib, 2),
      "volume_basis": basis,
      "top_services": top_services,
  }


def top_driver(top_services: Sequence[Dict[str, Any]]) -> Optional[str]:
  """The named service with the most estimated dollars, volume breaking ties."""
  # Vended GiB are cheaper, so the largest service by volume need not cost the
  # most. The remainder row is never a candidate.
  named = [s for s in top_services if not s.get("is_remainder")]
  if not named:
    return None
  return max(named, key=lambda s: (s["cost_usd"], s["gib"]))["service"]


def latest_complete_month(
    monthly: Mapping[str, Mapping[str, Any]],
) -> Optional[str]:
  """The newest month that has both ended and been fully observed."""
  return max(
      (m for m, e in monthly.items() if not e["is_partial"]), default=None
  )


def get_weekly_aggregations(
    parsed_billing: Dict[str, List[List[Any]]],
    now: datetime.datetime,
    price_book: PriceBook,
) -> Dict[str, Dict[str, Any]]:
  """Calculates 4 rolling 7-day weeks (W-1 to W-4) for WoW trend analysis.

  Args:
    parsed_billing: Daily `[date, bytes]` points keyed by service.
    now: Reference instant; W-1 is the seven days ending on its date.
    price_book: Prices each week at its average rate, so four weeks sum to about
      one monthly bill.

  Returns:
    A dict keyed `W-1` to `W-4` with dates, volume, cost, partial flag and
    per-service bytes.
  """
  rate = price_book.average_rate
  weeks: Dict[str, Dict[str, Any]] = {}
  for w_idx in range(1, 5):
    end_d = now - datetime.timedelta(days=(w_idx - 1) * 7)
    start_d = now - datetime.timedelta(days=w_idx * 7 - 1)
    start_str = start_d.strftime("%Y-%m-%d")
    end_str = end_d.strftime("%Y-%m-%d")

    w_bytes = 0
    w_services: Dict[str, int] = collections.defaultdict(int)
    for service, points in parsed_billing.items():
      for date_str, val in points:
        if start_str <= date_str <= end_str:
          w_bytes += val
          w_services[service] += val

    w_gib = w_bytes / BYTES_PER_GIB
    weeks[f"W-{w_idx}"] = {
        "start_date": start_str,
        "end_date": end_str,
        "total_bytes": w_bytes,
        "total_gib": round(w_gib, 2),
        "cost_usd": round(w_gib * rate, 2),
        # W-1 ends today, so it covers a partial final day and will always
        # look slightly lower than its neighbours.
        "is_partial": w_idx == 1,
        "services": dict(
            sorted(w_services.items(), key=lambda x: x[1], reverse=True)
        ),
    }

  return weeks


def get_daily_services(
    billing_data: Dict[str, List[List[Any]]],
    now: datetime.datetime,
    days: int = DEFAULT_SAMPLE_DAYS,
) -> Dict[str, Dict[str, int]]:
  """Extracts daily volume per service for the last N days."""
  start_date_str = window_start(now, days)
  daily_services: Dict[str, Dict[str, int]] = collections.defaultdict(
      lambda: collections.defaultdict(int)
  )
  for service, points in billing_data.items():
    for date_str, val in points:
      if date_str >= start_date_str:
        daily_services[date_str][service] += val

  return {
      d: dict(
          sorted(
              daily_services[d].items(),
              key=lambda x: x[1],
              reverse=True,
          )
      )
      for d in sorted(daily_services.keys())
  }


def get_mom_patterns(
    monthly_aggregations: Dict[str, Dict[str, Any]],
) -> Dict[str, Dict[str, Any]]:
  """Pre-computes Month-over-Month volume and cost growth patterns."""
  trends: Dict[str, Dict[str, Any]] = collections.defaultdict(dict)
  months = list(monthly_aggregations.keys())

  for i in range(1, len(months)):
    prev_month, curr_month = months[i - 1], months[i]
    period_key = f"{prev_month}_to_{curr_month}"

    prev_data = monthly_aggregations[prev_month]
    curr_data = monthly_aggregations[curr_month]

    prev_services = prev_data["services"]
    curr_services = curr_data["services"]
    all_services = set(prev_services.keys()) | set(curr_services.keys())

    prev_cost = prev_data["net_cost_usd"]
    curr_cost = curr_data["net_cost_usd"]
    cost_delta = round(curr_cost - prev_cost, 2)
    cost_pct_change = (
        "NEW"
        if prev_cost == 0
        else round(((curr_cost - prev_cost) / prev_cost) * 100, 1)
    )

    partial_sides = [
        f"{label} ({data['partial_reason']})"
        for label, data in ((prev_month, prev_data), (curr_month, curr_data))
        if data["is_partial"]
    ]

    total_entry: Dict[str, Any] = {
        "cost_change_usd": cost_delta,
        "cost_pct_change": cost_pct_change,
        # A comparison involving a partial month is not a trend; the UI
        # suppresses the percentage.
        "comparable": not partial_sides,
    }
    if partial_sides:
      total_entry["partial_warning"] = "Not directly comparable: " + "; ".join(
          partial_sides
      )

    trends["_monthly_total"][period_key] = total_entry

    for service in all_services:
      prev_val = prev_services.get(service, 0)
      curr_val = curr_services.get(service, 0)
      if prev_val == 0 and curr_val == 0:
        continue

      bytes_change = curr_val - prev_val
      pct_change = (
          "NEW" if prev_val == 0 else round((bytes_change / prev_val) * 100, 1)
      )
      trends[service][period_key] = {
          "bytes_change": bytes_change,
          "pct_change": pct_change,
      }

  return dict(trends)


def project_month(
    now: datetime.datetime,
    price_book: PriceBook,
    parsed_billing: Dict[str, List[List[Any]]],
    invoiced_daily_gib_by_sku: Optional[Dict[str, Dict[str, float]]] = None,
) -> Dict[str, Any]:
  """Projects this month's ingestion bill to month end, priced by the book.

  Each SKU's month-end GiB is its mean GiB/day over the month's complete days
  times the month's length, never less than month-to-date. Both figures are
  priced as whole months, so the free tier comes off once and only where it
  exists.

  Args:
    now: Reference instant; its calendar month is the one projected.
    price_book: Maps services to SKUs and prices both figures.
    parsed_billing: `billing/bytes_ingested` daily points per resource type;
      used when the invoice has no rows for this month yet.
    invoiced_daily_gib_by_sku: Invoiced ingestion GiB per SKU per Pacific day.

  Returns:
    The projected month, the month-to-date and end-of-month volume (total and
    per SKU) and cost, a `volume_basis`, and a human-readable note.
  """
  month = now.strftime("%Y-%m")
  invoiced = {
      sku: {d: g for d, g in days.items() if d.startswith(month)}
      for sku, days in (invoiced_daily_gib_by_sku or {}).items()
  }
  invoiced = {sku: days for sku, days in invoiced.items() if days}
  if invoiced:
    daily_by_sku = invoiced
    volume_basis = "invoiced_daily_usage"
  else:
    daily_by_sku = collections.defaultdict(
        lambda: collections.defaultdict(float)
    )
    for service, points in parsed_billing.items():
      sku = price_book.sku_for_resource(service)
      for day, num_bytes in points:
        if day.startswith(month):
          daily_by_sku[sku][day] += num_bytes / BYTES_PER_GIB
    volume_basis = "cloud_monitoring_metric"

  so_far_by_sku: Dict[str, float] = {}
  eom_by_sku: Dict[str, float] = {}
  for sku, days in daily_by_sku.items():
    # Cloud Monitoring returns only whole UTC days; the invoice's latest day
    # can still be filling in, so it must not drag the mean down.
    complete = complete_days(days, month, now) if invoiced else days
    so_far_by_sku[sku] = sum(days.values())
    per_day = sum(complete.values()) / len(complete) if complete else 0.0
    eom_by_sku[sku] = max(so_far_by_sku[sku], per_day * _month_span(month))
  so_far_by_sku = price_book.collapse(so_far_by_sku)
  eom_by_sku = price_book.collapse(eom_by_sku)

  return {
      "month": month,
      "projection_method": "linear_monthly_run_rate",
      "volume_basis": volume_basis,
      "so_far_gib": round(sum(so_far_by_sku.values()), 2),
      "projected_eom_gib": round(sum(eom_by_sku.values()), 2),
      "so_far_gib_by_sku": {k: round(v, 2) for k, v in so_far_by_sku.items()},
      "projected_eom_gib_by_sku": {
          k: round(v, 2) for k, v in eom_by_sku.items()
      },
      "so_far_cost_usd": price_book.month_cost(so_far_by_sku),
      "projected_eom_cost_usd": price_book.month_cost(eom_by_sku),
      "confidence_note": (
          f"Cost projected per SKU ({price_book.formula_terms()}), before"
          " credits."
      ),
  }
