"""Re-measures a report claim live, using the queries its Prove It panel shows.

    python3 verify_claim.py --summary logging_usage_summary.json --claim
    top_cost_driver
    python3 verify_claim.py --summary logging_usage_summary.json --claim all

Runs each claim's `checks` (SQL, PromQL or Monitoring filter) live and prints
reported vs. current values against the tolerance each check carries. Drift is
reported; only a failure to run a check exits non-zero.
"""

import argparse
import concurrent.futures
import datetime
import json
import sys
from typing import Any, Callable, Dict, List, NamedTuple, Optional

import attribution
from google.cloud import monitoring_v3
import monitoring

# Concurrent Monitoring reads per check; modest to respect read quota.
MONITORING_SUM_WORKERS = 16


def _pct_delta(expected: float, measured: float) -> float:
  if not expected:
    return 0.0 if not measured else 100.0
  return (measured - expected) / abs(expected) * 100.0


def _parse_ts(value: str) -> datetime.datetime:
  return datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))


# ==============================================================================
# Source runners (injectable for tests)
# ==============================================================================


def run_bigquery(query: str, project: Optional[str]) -> List[Dict[str, Any]]:
  from google.cloud import bigquery  # pylint: disable=g-import-not-at-top

  client = bigquery.Client(
      project=project,
      client_info=attribution.client_info(attribution.VERIFY_CLAIM),
  )
  return [dict(row) for row in client.query(query).result()]


def run_promql(project: str, query: str, time: str) -> Dict[str, float]:
  """Evaluates an instant PromQL query; returns {label-set: value}."""
  import google.auth  # pylint: disable=g-import-not-at-top
  from google.auth.transport.requests import AuthorizedSession  # pylint: disable=g-import-not-at-top

  creds, _ = google.auth.default(
      scopes=["https://www.googleapis.com/auth/monitoring.read"]
  )
  url = (
      "https://monitoring.googleapis.com/v1/projects/"
      f"{project}/location/global/prometheus/api/v1/query"
  )
  session = attribution.tag_session(
      AuthorizedSession(creds), attribution.VERIFY_CLAIM
  )
  resp = session.post(url, data={"query": query, "time": time})
  body = resp.json()
  if resp.status_code != 200 or body.get("status") != "success":
    raise RuntimeError(body.get("error") or resp.text[:300])
  out: Dict[str, float] = {}
  for item in body["data"]["result"]:
    key = json.dumps(item.get("metric", {}), sort_keys=True)
    out[key] = float(item["value"][1])
  return out


def run_monitoring_sum(project: str, flt: str, start: str, end: str) -> float:
  """Σ bytes for one filter, in daily buckets like the collector."""
  client = monitoring_v3.MetricServiceClient(
      client_info=attribution.client_info(attribution.VERIFY_CLAIM)
  )
  s, e = _parse_ts(start), _parse_ts(end)
  return monitoring.sum_filter(client, project, flt, e, (e - s).days)


class Runners(NamedTuple):
  """The live query runners; tests replace them with fakes."""

  bigquery: Callable[..., List[Dict[str, Any]]] = run_bigquery
  promql: Callable[..., Dict[str, float]] = run_promql
  monitoring_sum: Callable[..., float] = run_monitoring_sum


# ==============================================================================
# Check evaluation
# ==============================================================================


def _row(
    key: str,
    expected: float,
    measured: float,
    unit: str,
    tol: float,
    points: bool = False,
) -> Dict[str, Any]:
  delta = (measured - expected) if points else _pct_delta(expected, measured)
  return {
      "key": key,
      "expected": expected,
      "measured": round(measured, 4),
      "unit": unit,
      "delta": round(delta, 2),
      "delta_unit": "points" if points else "%",
      "ok": abs(delta) <= tol,
  }


def _label_value(key_json: str, label: str) -> str:
  return json.loads(key_json).get(label, "")


def evaluate_check(
    check: Dict[str, Any], project: str, runners: Runners
) -> Dict[str, Any]:
  """Runs one check and compares it with what the report printed."""
  kind = check.get("kind")
  rows: List[Dict[str, Any]] = []
  try:
    if kind == "bigquery":
      result = runners.bigquery(check["query"], check.get("project"))
      if check.get("compare") == "share_rows":
        got = {
            str(r[check["row_key"]]): float(r[check["row_value"]] or 0)
            for r in result
        }
        tol = check["tolerance_points"]
        for k, exp in check["expect"].items():
          rows.append(_row(k, exp, got.get(k, 0.0), "%", tol, points=True))
      else:
        # Row one: a single-row query, or the ROLLUP total sorted first.
        first = result[0]
        for k, exp in check["expect"].items():
          if exp is None:
            continue
          rows.append(
              _row(k, exp, float(first[k] or 0), "", check["tolerance_pct"])
          )
    elif kind == "promql":
      result = runners.promql(project, check["query"], check["time"])
      by_label = {
          _label_value(k, check.get("label_key", "")): v
          for k, v in result.items()
      }
      if check.get("compare") == "total":
        # `sum(...)` returns one unlabeled series; add up everything.
        rows.append(
            _row(
                "total",
                check["expect"]["total"],
                sum(result.values()) * check.get("scale", 1.0),
                check.get("unit", "GiB"),
                check["tolerance_pct"],
            )
        )
      elif check.get("compare") == "share":
        total = sum(by_label.values()) or 1.0
        tol = check["tolerance_points"]
        for k, exp in check["expect"].items():
          rows.append(
              _row(
                  k,
                  exp,
                  by_label.get(k, 0.0) / total * 100,
                  "%",
                  tol,
                  points=True,
              )
          )
      else:
        scale = check.get("scale", 1.0)
        tol = check["tolerance_pct"]
        for k, exp in check["expect"].items():
          rows.append(_row(k, exp, by_label.get(k, 0.0) * scale, "GiB", tol))
    elif kind == "monitoring_sum":
      series = check["series"]
      # One independent read per claimed stream, run concurrently.
      with concurrent.futures.ThreadPoolExecutor(
          max_workers=min(MONITORING_SUM_WORKERS, max(len(series), 1))
      ) as pool:
        total = sum(
            pool.map(
                lambda s: runners.monitoring_sum(
                    project, s["filter"], check["start"], check["end"]
                ),
                series,
            )
        )
      measured = total * check.get("multiplier", 1.0)
      rows.append(
          _row(
              "total",
              check["expect"]["total"],
              measured,
              check.get("unit", ""),
              check["tolerance_pct"],
          )
      )
    else:
      raise ValueError(f"unknown check kind {kind!r}")
  except Exception as e:  # pylint: disable=broad-except
    return {
        "label": check.get("label"),
        "kind": kind,
        "error": str(e),
        "rows": [],
    }
  return {
      "label": check.get("label"),
      "kind": kind,
      "rows": rows,
      "ok": all(r["ok"] for r in rows),
  }


def verify(
    summary: Dict[str, Any], claim_ids: List[str], runners: Runners
) -> List[Dict[str, Any]]:
  """Runs each claim's recorded checks against the live sources.

  Args:
    summary: The collected summary holding a `provenance` block.
    claim_ids: Claim IDs to check, or `["all"]`.
    runners: The query runners to execute each check with.

  Returns:
    One result per claim: its checks' outcomes and recorded differences, or an
    `error` when the claim is unknown.
  """
  claims = summary["provenance"]["claims"]
  project = summary["project_id"]
  if claim_ids == ["all"]:
    claim_ids = list(claims)
  # A claim built from others (the floor from its actions) re-checks them too.
  for cid in list(claim_ids):
    if cid in claims:
      claim_ids += [r for r in claims[cid]["see_also"] if r not in claim_ids]
  out = []
  for cid in claim_ids:
    claim = claims.get(cid)
    if not claim:
      out.append({"claim": cid, "error": "no such claim in provenance"})
      continue
    results = [evaluate_check(c, project, runners) for c in claim["checks"]]
    out.append({
        "claim": cid,
        "title": claim["title"],
        "value": claim["value"],
        "checks": results,
        "differences": claim["differences"],
    })
  return out


def render(results: List[Dict[str, Any]]) -> str:
  """Formats `verify` results as one ✓/✗ line per check, for the chat."""
  lines = []
  for res in results:
    if res.get("error"):
      lines.append(f"✗ {res['claim']}: {res['error']}")
      continue
    lines.append(f"■ {res['title']} — report says {res['value']}")
    if not res["checks"]:
      lines.append("  (no live check for this claim; see its sources)")
    for chk in res["checks"]:
      if chk.get("error"):
        lines.append(f"  ✗ {chk['label']}: could not run — {chk['error']}")
        continue
      for r in chk["rows"]:
        mark = "✓" if r["ok"] else "△"
        lines.append(
            f"  {mark} {chk['label']} [{r['key']}]: report {r['expected']}"
            f" · now {r['measured']} {r['unit']}".rstrip()
            + f" · Δ {r['delta']:+} {r['delta_unit']}"
        )
  return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
  parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
  parser.add_argument("--summary", default="logging_usage_summary.json")
  parser.add_argument(
      "--claim",
      action="append",
      required=True,
      help="Claim id (repeatable), or 'all'.",
  )
  parser.add_argument(
      "--json", action="store_true", help="Print machine-readable results."
  )
  args = parser.parse_args(argv)
  with open(args.summary, encoding="utf-8") as f:
    summary = json.load(f)
  results = verify(summary, args.claim, Runners())
  print(json.dumps(results, indent=2) if args.json else render(results))
  errored = any(
      r.get("error") or any(c.get("error") for c in r.get("checks", []))
      for r in results
  )
  return 1 if errored else 0


if __name__ == "__main__":
  sys.exit(main())
