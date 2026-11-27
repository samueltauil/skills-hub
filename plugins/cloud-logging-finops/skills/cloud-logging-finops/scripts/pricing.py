"""Per-SKU Cloud Logging ingestion pricing.

Log Storage: $0.50/GiB, first 50 GiB per project per month free.
Vended Logs Storage: $0.25/GiB, no free tier (VPC Flow, Firewall, Cloud NAT).

A `PriceBook` prices bills and savings per SKU, falling back to one blended
rate when telemetry's vended share disagrees with the invoice's.
"""

import dataclasses
import datetime
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple
import urllib.parse

from constants import billable_gib
from constants import FREE_TIER_GIB_PER_MONTH
from constants import LIST_PRICE_PER_GIB
from constants import PLAUSIBLE_RATE_RANGE_PER_GIB
from constants import price_reduction

LOG_STORAGE = "log_storage"
VENDED = "vended"
BLENDED = "blended"

VENDED_LIST_PRICE_PER_GIB = 0.25

SKU_LABELS = {
    LOG_STORAGE: "Log Storage",
    VENDED: "Vended Logs Storage",
    BLENDED: "All ingestion (blended)",
}

# (list unit price, free GiB per project per month)
SKU_LIST_TERMS = {
    LOG_STORAGE: (LIST_PRICE_PER_GIB, FREE_TIER_GIB_PER_MONTH),
    VENDED: (VENDED_LIST_PRICE_PER_GIB, 0.0),
}

# Log ID suffixes of the vended network logs. The suffix, not the full ID,
# because VPC Flow Logs are written under both `compute.googleapis.com` and
# `networkmanagement.googleapis.com`.
VENDED_LOG_SUFFIXES = frozenset({"vpc_flows", "firewall", "nat_flows"})

# Monitored resource types that carry only vended network logs. Flow and
# firewall logs are written against `gce_subnetwork`; flow logs configured
# through Network Management against `vpc_flow_logs_config`; NAT logs against
# `nat_gateway`.
VENDED_RESOURCE_TYPES = frozenset(
    {"vpc_flow_logs_config", "gce_subnetwork", "nat_gateway"}
)

# Max gap between telemetry's and the invoice's vended share before the
# stream-to-SKU mapping is distrusted. Loose: catches wrong, not noisy.
MAPPING_TOLERANCE_POINTS = 15.0

# A SKU month billing less than this many GiB above its free allotment is too
# small to derive a unit price from; cents rounding dominates.
_MIN_PRICED_GIB = 1.0


def sku_of_description(description: str) -> str:
  """Maps a billing export `sku.description` to a SKU key."""
  return VENDED if "vended" in (description or "").lower() else LOG_STORAGE


def sku_of_log(log_id: str) -> str:
  """Maps a log ID (URL-encoded or not) to the SKU that bills it."""
  suffix = urllib.parse.unquote(log_id or "").rsplit("/", 1)[-1].lower()
  return VENDED if suffix in VENDED_LOG_SUFFIXES else LOG_STORAGE


def sku_of_resource(resource_type: str) -> str:
  """Maps a monitored resource type to the SKU that bills its logs."""
  return VENDED if resource_type in VENDED_RESOURCE_TYPES else LOG_STORAGE


@dataclasses.dataclass
class SkuTerms:
  """One SKU's price, free allotment and share of the monthly baseline."""

  unit_price: float
  free_gib: float
  baseline_gib: float
  price_source: str  # "invoice" or "list"
  price_month: Optional[str] = None

  def month_cost(self, gib: float) -> float:
    return round(billable_gib(gib, self.free_gib) * self.unit_price, 2)

  @property
  def baseline_cost(self) -> float:
    return self.month_cost(self.baseline_gib)

  @property
  def effective_rate(self) -> float:
    """Baseline cost per baseline GiB, free allotment included."""
    if self.baseline_gib <= 0:
      return self.unit_price
    return self.baseline_cost / self.baseline_gib


class PriceBook:
  """Prices ingestion, and reductions in it, per billing SKU."""

  def __init__(
      self,
      skus: Dict[str, SkuTerms],
      mode: str,
      notes: Optional[Iterable[str]] = None,
      mapping_check: Optional[Dict[str, Any]] = None,
  ) -> None:
    self.skus = skus
    self.mode = mode  # "per_sku" or "blended"
    self.notes = list(notes or [])
    self.mapping_check = mapping_check or {}

  # --- construction --------------------------------------------------------

  @classmethod
  def blended(
      cls,
      rate_per_gib: float,
      baseline_gib: float,
      price_source: str = "list",
      notes: Optional[Iterable[str]] = None,
      mapping_check: Optional[Dict[str, Any]] = None,
  ) -> "PriceBook":
    """One rate for every GiB; the fallback when per-SKU is untrusted."""
    return cls(
        {
            BLENDED: SkuTerms(
                unit_price=rate_per_gib,
                free_gib=FREE_TIER_GIB_PER_MONTH,
                baseline_gib=max(0.0, baseline_gib or 0.0),
                price_source=price_source,
            )
        },
        mode="blended",
        notes=notes,
        mapping_check=mapping_check,
    )

  @classmethod
  def from_dict(cls, data: Mapping[str, Any]) -> "PriceBook":
    """Rebuilds a book from its `to_dict()` form (e.g. a saved summary)."""
    skus = {
        key: SkuTerms(
            unit_price=float(v["unit_price_per_gib"]),
            free_gib=float(v["free_gib"]),
            baseline_gib=float(v["baseline_monthly_gib"]),
            price_source=v["price_source"],
            price_month=v["price_month"],
        )
        for key, v in data["skus"].items()
    }
    return cls(
        skus,
        mode=data["mode"],
        notes=data["notes"],
        mapping_check=data["mapping_check"],
    )

  # --- mapping -------------------------------------------------------------

  @property
  def per_sku(self) -> bool:
    return self.mode == "per_sku"

  def sku_for_log(self, log_id: str) -> str:
    return sku_of_log(log_id) if self.per_sku else BLENDED

  def sku_for_resource(self, resource_type: str) -> str:
    return sku_of_resource(resource_type) if self.per_sku else BLENDED

  def terms(self, sku: str) -> SkuTerms:
    if sku in self.skus:
      return self.skus[sku]
    # A stream on a SKU the invoice never billed (e.g. a new firewall log on a
    # project with no vended history) is priced at that SKU's list terms.
    price, free = SKU_LIST_TERMS.get(sku, (LIST_PRICE_PER_GIB, 0.0))
    return SkuTerms(price, free, 0.0, "list")

  # --- pricing -------------------------------------------------------------

  @property
  def baseline_gib(self) -> float:
    return sum(t.baseline_gib for t in self.skus.values())

  @property
  def baseline_cost(self) -> float:
    return round(sum(t.baseline_cost for t in self.skus.values()), 2)

  @property
  def average_rate(self) -> float:
    """Baseline bill per baseline GiB across all SKUs, free tier included.

    For figures that cannot be split by SKU (e.g. a week's total volume), so
    they sum to the monthly bill.
    """
    gib = self.baseline_gib
    return self.baseline_cost / gib if gib > 0 else 0.0

  def collapse(self, gib_by_sku: Mapping[str, float]) -> Dict[str, float]:
    """Re-keys per-SKU volumes onto this book's SKUs."""
    # A blended book prices every GiB on its one SKU, so per-SKU input (e.g.
    # invoiced daily GiB) is summed onto it rather than priced at list terms.
    if self.per_sku:
      return dict(gib_by_sku)
    return {BLENDED: sum(gib_by_sku.values())}

  def month_cost(self, gib_by_sku: Mapping[str, float]) -> float:
    """Returns a whole month's bill for the given per-SKU volumes."""
    return round(
        sum(self.terms(k).month_cost(g) for k, g in gib_by_sku.items()), 2
    )

  def saving(self, removed_by_sku: Mapping[str, float]) -> float:
    """Returns the monthly saving from removing per-SKU monthly GiB."""
    # Each SKU is priced as the difference of two bills, so the free tier
    # applies only where it exists.
    total = 0.0
    for sku, removed in removed_by_sku.items():
      if not removed:
        continue
      terms = self.terms(sku)
      # Clamped to the SKU's own baseline by `price_reduction`: a saving can
      # never exceed what that SKU is billed.
      total += price_reduction(
          removed_gib=removed,
          baseline_monthly_gib=terms.baseline_gib,
          rate_per_gib=terms.unit_price,
          free_tier_gib=terms.free_gib,
      )
    return round(total, 2)

  def split_by_logs(
      self, total_gib: float, weights: Iterable[Tuple[str, float]]
  ) -> Dict[str, float]:
    """Splits `total_gib` across SKUs in proportion to per-log weights.

    Args:
      total_gib: Monthly GiB to split.
      weights: `(log_id, weight)` pairs, e.g. each claimed stream's bytes.

    Returns:
      Monthly GiB keyed by SKU. All on one SKU when no weights are given.
    """
    by_sku: Dict[str, float] = {}
    for log_id, weight in weights:
      if weight and weight > 0:
        sku = self.sku_for_log(log_id)
        by_sku[sku] = by_sku.get(sku, 0.0) + weight
    denom = sum(by_sku.values())
    if denom <= 0:
      return {self.sku_for_log(""): total_gib}
    return {k: total_gib * w / denom for k, w in by_sku.items()}

  def saving_for_logs(
      self, total_gib: float, weights: Iterable[Tuple[str, float]]
  ) -> float:
    return self.saving(self.split_by_logs(total_gib, weights))

  def pct_of_spend(self, saving_usd: float) -> float:
    cost = self.baseline_cost
    return round(100.0 * saving_usd / cost, 2) if cost > 0 else 0.0

  def service_cost(self, resource_type: str, monthly_gib: float) -> float:
    """Estimated monthly dollars for one service at its SKU's effective rate."""
    # The effective rate spreads the Log Storage free tier across all its GiB.
    terms = self.terms(self.sku_for_resource(resource_type))
    return round(max(0.0, monthly_gib) * terms.effective_rate, 2)

  # --- publication ---------------------------------------------------------

  def formula_terms(self) -> str:
    """Human-readable per-SKU terms, for Prove It and evidence prose."""
    parts = []
    for sku, t in self.skus.items():
      free = (
          f", first {t.free_gib:g} GiB free" if t.free_gib else ", no free tier"
      )
      parts.append(f"{SKU_LABELS.get(sku, sku)} ${t.unit_price:.4g}/GiB{free}")
    return "; ".join(parts)

  def to_dict(self) -> Dict[str, Any]:
    return {
        "mode": self.mode,
        "baseline_monthly_gib": round(self.baseline_gib, 2),
        "baseline_monthly_cost_usd": self.baseline_cost,
        "skus": {
            key: {
                "label": SKU_LABELS.get(key, key),
                "unit_price_per_gib": round(t.unit_price, 4),
                "free_gib": t.free_gib,
                "baseline_monthly_gib": round(t.baseline_gib, 2),
                "baseline_monthly_cost_usd": t.baseline_cost,
                "effective_rate_per_gib": round(t.effective_rate, 4),
                "price_source": t.price_source,
                "price_month": t.price_month,
            }
            for key, t in self.skus.items()
        },
        "vended_resource_types": sorted(VENDED_RESOURCE_TYPES),
        "mapping_check": self.mapping_check,
        "notes": self.notes,
    }


# ==============================================================================
# Construction from the billing export
# ==============================================================================


def invoiced_unit_prices(
    monthly_costs: Mapping[str, Mapping[str, Any]],
    current_month: Optional[str] = None,
) -> Dict[str, Tuple[float, str, Optional[str]]]:
  """Derives each SKU's unit price from the invoice, else its list price.

  Price is raw (pre-credit) cost over billable GiB (after the free tier), so
  the free tier is not counted twice when pricing savings.

  Args:
    monthly_costs: `billing.query_logging_billing_costs()["monthly_costs"]`.
    current_month: The in-progress month, used only when no complete month
      priced a SKU.

  Returns:
    `{sku: (unit_price, "invoice" | "list", month or None)}` for both SKUs.
  """
  low, high = PLAUSIBLE_RATE_RANGE_PER_GIB
  prices: Dict[str, Tuple[float, str, Optional[str]]] = {}
  months = sorted(monthly_costs, reverse=True)
  # Complete months first; the current month only as a last resort.
  ordered = [m for m in months if m != current_month] + [
      m for m in months if m == current_month
  ]
  for sku, (list_price, free) in SKU_LIST_TERMS.items():
    for month in ordered:
      entry = monthly_costs[month]["ingestion_by_sku"].get(sku)
      if not entry:
        continue
      billable = billable_gib(entry["gib"], free)
      if billable < _MIN_PRICED_GIB:
        continue
      unit = entry["raw_cost_usd"] / billable
      if low <= unit <= high:
        prices[sku] = (round(unit, 4), "invoice", month)
        break
    prices.setdefault(sku, (list_price, "list", None))
  return prices


def last_complete_invoice_day(now: datetime.datetime) -> datetime.date:
  """The latest invoice day fully billed by `now`."""
  # Invoice days are Pacific, so day D is complete at D+1 08:00 UTC.
  return (now - datetime.timedelta(days=1, hours=8)).date()


def complete_days(
    daily: Optional[Mapping[str, float]], start: str, now: datetime.datetime
) -> Dict[str, float]:
  """The `{YYYY-MM-DD: value}` invoice days from `start` that are complete."""
  last = last_complete_invoice_day(now).isoformat()
  return {d: v for d, v in (daily or {}).items() if start <= d <= last}


def invoiced_sku_shares(
    daily_gib_by_sku: Optional[Mapping[str, Mapping[str, float]]],
    window_start: str,
    now: datetime.datetime,
) -> Optional[Dict[str, float]]:
  """Returns each SKU's share of invoiced GiB over complete window days."""
  if not daily_gib_by_sku:
    return None
  sums = {
      sku: sum(complete_days(days, window_start, now).values())
      for sku, days in daily_gib_by_sku.items()
  }
  total = sum(sums.values())
  if total <= 0:
    return None
  return {sku: v / total for sku, v in sums.items() if v > 0}


def telemetry_vended_share(
    bytes_by_stream: Optional[Mapping[Tuple[str, str], float]],
) -> Optional[float]:
  """Returns the share of `byte_count` bytes on streams mapped to Vended."""
  if not bytes_by_stream:
    return None
  total = sum(bytes_by_stream.values())
  if total <= 0:
    return None
  vended = sum(
      v
      for (log_id, _), v in bytes_by_stream.items()
      if sku_of_log(log_id) == VENDED
  )
  return vended / total


def build_price_book(
    baseline_gib: float,
    now: datetime.datetime,
    window_start: str,
    monthly_costs: Optional[Mapping[str, Mapping[str, Any]]] = None,
    daily_gib_by_sku: Optional[Mapping[str, Mapping[str, float]]] = None,
    bytes_by_stream: Optional[Mapping[Tuple[str, str], float]] = None,
) -> PriceBook:
  """Builds the price book every dollar figure in the report is priced from.

  Args:
    baseline_gib: The gross monthly ingestion run rate, all SKUs.
    now: Reference instant; see `last_complete_invoice_day`.
    window_start: First date (`YYYY-MM-DD`) of the run-rate window.
    monthly_costs: Invoiced months, carrying `ingestion_by_sku`.
    daily_gib_by_sku: Invoiced ingestion GiB per SKU per Pacific day.
    bytes_by_stream: `byte_count` bytes keyed by `(log_id, severity)`, used to
      check the stream-to-SKU mapping and, without an invoice, to split the
      baseline.

  Returns:
    A per-SKU `PriceBook`, or a blended one with the reason in `notes`.
  """
  current_month = now.strftime("%Y-%m")
  prices = invoiced_unit_prices(monthly_costs or {}, current_month)
  invoice_shares = invoiced_sku_shares(daily_gib_by_sku, window_start, now)
  tele_vended = telemetry_vended_share(bytes_by_stream)

  check: Dict[str, Any] = {
      "invoice_vended_share_pct": (
          round(100.0 * invoice_shares.get(VENDED, 0.0), 1)
          if invoice_shares
          else None
      ),
      "telemetry_vended_share_pct": (
          round(100.0 * tele_vended, 1) if tele_vended is not None else None
      ),
  }

  if invoice_shares:
    shares = invoice_shares
    split_source = "billing_export"
  elif tele_vended is not None:
    shares = {VENDED: tele_vended, LOG_STORAGE: 1.0 - tele_vended}
    split_source = "cloud_monitoring_byte_count"
  else:
    return PriceBook.blended(
        LIST_PRICE_PER_GIB,
        baseline_gib,
        notes=["No per-SKU volume available; priced at one blended rate."],
        mapping_check=check,
    )
  check["split_source"] = split_source

  if invoice_shares and tele_vended is not None:
    gap = abs(100.0 * invoice_shares.get(VENDED, 0.0) - 100.0 * tele_vended)
    check["gap_points"] = round(gap, 1)
    check["passed"] = gap <= MAPPING_TOLERANCE_POINTS
    if not check["passed"]:
      # The baseline split holds but per-stream SKUs are untrusted, so price
      # every GiB at one blended rate.
      billable = billable_gib(baseline_gib)
      invoiced_cost = sum(
          billable_gib(baseline_gib * shares.get(k, 0.0), SKU_LIST_TERMS[k][1])
          * prices[k][0]
          for k in SKU_LIST_TERMS
      )
      rate = invoiced_cost / billable if billable > 0 else LIST_PRICE_PER_GIB
      return PriceBook.blended(
          round(rate, 4),
          baseline_gib,
          price_source="invoice",
          notes=[
              f"Telemetry puts {check['telemetry_vended_share_pct']}% of"
              " volume on vended network logs but the invoice bills"
              f" {check['invoice_vended_share_pct']}% as Vended Logs Storage;"
              " the stream-to-SKU mapping was not trusted, so every GiB is"
              " priced at one blended rate."
          ],
          mapping_check=check,
      )

  skus = {}
  for sku, (price, source, month) in prices.items():
    share = shares.get(sku, 0.0)
    if share <= 0 and sku != LOG_STORAGE:
      continue
    skus[sku] = SkuTerms(
        unit_price=price,
        free_gib=SKU_LIST_TERMS[sku][1],
        baseline_gib=baseline_gib * share,
        price_source=source,
        price_month=month,
    )
  return PriceBook(skus, mode="per_sku", mapping_check=check)
