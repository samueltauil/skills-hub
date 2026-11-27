#!/bin/bash
# Arm an Apigee debug session, and read it back as the verify.md checklist.
#
# references/verify.md lists nine things to confirm on a governed turn. Every
# one of them was a hand-written JSON parse until this script existed, and the
# transaction shape is not guessable: flow variables live under
#   point[].results[].ActionResult == "VariableAccess"
# in an accessList of {Get|Set: {name, value}} objects, while step execution
# lives under
#   point[].id == "Execution", results[].ActionResult == "DebugInfo"
# with properties stepDefinition-name / expressionResult / action. Step
# conditions do NOT surface as Condition points -- those carry only
# ("default" equals proxy.name) -- so "did this step run" has to be read off
# Execution, not off a condition result.
#
# The first parse attempt against a healthy trace returning nothing is the
# normal experience, and it sends you to debug the callout when the parser is
# what is broken.
#
# Two modes:
#   --arm    create a session and print its ABSOLUTE expiry, read back off the
#            response rather than echoed from the request (see below)
#   default  fetch /data, fetch each transaction, print the checklist
#
# Data goes to stdout. Diagnostics go to stderr.

set -euo pipefail

usage() {
  cat <<'EOF'
Arm and read an Apigee debug session for the governance proxy.

Usage:
  read_debug_session.sh --org O --env E --proxy P --rev R --arm [options]
  read_debug_session.sh --org O --env E --proxy P --rev R --session S [options]

Required:
  --org ORG              Apigee org
  --env ENV              environment hosting the proxy
  --proxy PROXY          proxy name
  --rev REV              revision number

Mode:
  --arm                  create a session, print its id and absolute expiry
  --session S            read this session back (omit --arm)

Options (--arm):
  --count N              transactions to capture; min 1, max 15, default 10
  --tracesize N          max 5120 (default)
  --timeout N            seconds; min 60, max 600. SEE THE CLAMP NOTE BELOW
  --filter EXPR          flow-Condition expression; default captures model
                         calls only. Pass '' to capture everything
Options (read):
  --steps                also print executed-vs-skipped per policy
  --json                 machine-readable

Exit status:
  0  session read (including a legitimately empty one)
  1  no transactions AND the refusal-probe advice applies
  2  bad invocation
EOF
}

ORG=""; ENVNAME=""; PROXY=""; REV=""; SESSION=""; ARM=0
COUNT=10; TRACESIZE=5120; TIMEOUT=600; STEPS=0; JSON=0
FILTER='(request.uri Like "*generateContent*")'


while [[ $# -gt 0 ]]; do
  case "$1" in
    --org)       ORG="$2"; shift 2 ;;
    --env)       ENVNAME="$2"; shift 2 ;;
    --proxy)     PROXY="$2"; shift 2 ;;
    --rev)       REV="$2"; shift 2 ;;
    --session)   SESSION="$2"; shift 2 ;;
    --arm)       ARM=1; shift ;;
    --count)     COUNT="$2"; shift 2 ;;
    --tracesize) TRACESIZE="$2"; shift 2 ;;
    --timeout)   TIMEOUT="$2"; shift 2 ;;
    --filter)    FILTER="$2"; shift 2 ;;
    --steps)     STEPS=1; shift ;;
    --json)      JSON=1; shift ;;
    --help)      usage; exit 0 ;;
    *) echo "unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done

[[ -n "$ORG" && -n "$ENVNAME" && -n "$PROXY" && -n "$REV" ]] || { usage >&2; exit 2; }
[[ $ARM -eq 1 || -n "$SESSION" ]] || { echo "need --arm or --session" >&2; usage >&2; exit 2; }

# Colour on fd 1: this script's tables ARE its stdout, as in
# assess_integration.sh. The ensure_*/deploy_* scripts test fd 2 because they
# log progress to stderr. Each tests the stream it writes to.
if [[ -t 1 && -z "${NO_COLOR:-}" && "${TERM:-dumb}" != "dumb" ]]; then
  C_RST=$'\033[0m'; C_DIM=$'\033[2m'; C_BLD=$'\033[1m'
  C_GRN=$'\033[32m'; C_RED=$'\033[31m'; C_YEL=$'\033[33m'; C_BLU=$'\033[36m'
else
  C_RST=; C_DIM=; C_BLD=; C_GRN=; C_RED=; C_YEL=; C_BLU=
fi

# Byte-identical to the helper in the other five scripts: rule fills to 92
# past the title, so every header in the skill is 96 columns wide.
hdr() { printf '\n%s┌─ %s %s%s\n' "$C_DIM" "$1" "$(printf '─%.0s' $(seq 1 $(( 92 > ${#1} ? 92 - ${#1} : 3 ))))" "$C_RST"; }
log() { printf '%s\n' "$*" >&2; }
die() { printf '%s\n' "$*" >&2; exit "${2:-1}"; }

# ADC, not `gcloud auth print-access-token`: a plain gcloud token is rejected
# by apigee.googleapis.com on corp accounts with
# 401 ACCESS_TOKEN_TYPE_UNSUPPORTED ("restricted due to a domain admin's
# policies"). Same choice as assess_integration.sh.
TOKEN="$(gcloud auth application-default print-access-token 2>/dev/null || true)"
[[ -n "$TOKEN" ]] || die "no ADC token; run: gcloud auth application-default login" 2

BASE="https://apigee.googleapis.com/v1/organizations/$ORG/environments/$ENVNAME/apis/$PROXY/revisions/$REV/debugsessions"

# --------------------------------------------------------------------- arm --
if [[ $ARM -eq 1 ]]; then
  BODY="{\"count\":$COUNT,\"tracesize\":$TRACESIZE"
  [[ -n "$FILTER" ]] && BODY="$BODY,\"filter\":$(printf '%s' "$FILTER" | python3 -c 'import json,sys;print(json.dumps(sys.stdin.read()))')"
  BODY="$BODY}"

  RESP="$(curl -s -X POST -H "Authorization: Bearer $TOKEN" \
    -H 'Content-Type: application/json' "$BASE?timeout=$TIMEOUT" -d "$BODY" || true)"

  # THE POINT OF THIS MODE. 600 is what the API validates against, not
  # necessarily what you get: on a PAYG org ?timeout=600 is accepted silently
  # and comes back validity=300. Echoing the requested value is how you end up
  # believing you have ten minutes to go drive a turn by hand, getting five,
  # and reading the resulting empty session as "the callout is not landing".
  # So the expiry printed here is computed from what the SERVER returned.
  python3 - "$RESP" "$TIMEOUT" <<'PY'
import json, sys, time, datetime
raw, asked = sys.argv[1], int(sys.argv[2])
try:
    d = json.loads(raw)
except Exception:
    sys.stderr.write("could not parse create response:\n%s\n" % raw[:600]); sys.exit(2)
if "name" not in d:
    sys.stderr.write("session not created:\n%s\n" % json.dumps(d, indent=2)[:900]); sys.exit(2)
sid = d["name"].rsplit("/", 1)[-1]
validity = int(d.get("validity") or d.get("timeout") or 0)
expiry = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=validity)
print("session   %s" % sid)
print("validity  %ss" % validity, end="")
print("   <-- CLAMPED from the %ss requested" % asked if validity and validity < asked else "")
print("window    closes %s UTC  (local %s)" % (
    expiry.strftime("%H:%M:%S"), expiry.astimezone().strftime("%H:%M:%S")))
PY
  exit 0
fi

# -------------------------------------------------------------------- read --
# /data returns a BARE JSON LIST of transaction ids, not an object. A helper
# written as d.get("responses") or d.get("data") raises AttributeError on
# exactly that, which sends you to debug your own parser. Both shapes handled.
IDS_RAW="$(curl -s -H "Authorization: Bearer $TOKEN" "$BASE/$SESSION/data" || true)"

TXN_JSON="$(mktemp)"; trap 'rm -f "$TXN_JSON"' EXIT
printf '[' >"$TXN_JSON"
FIRST=1
for id in $(python3 -c '
import json,sys
try: d=json.loads(sys.argv[1])
except Exception: d=[]
ids = d if isinstance(d,list) else (d.get("responses") or d.get("data") or [])
print("\n".join(str(i) for i in ids))' "$IDS_RAW"); do
  T="$(curl -s -H "Authorization: Bearer $TOKEN" "$BASE/$SESSION/data/$id" || true)"
  [[ -z "$T" ]] && continue
  [[ $FIRST -eq 1 ]] || printf ',' >>"$TXN_JSON"
  printf '{"id":"%s","txn":%s}' "$id" "$T" >>"$TXN_JSON"
  FIRST=0
done
printf ']' >>"$TXN_JSON"

python3 - "$TXN_JSON" "$STEPS" "$JSON" "$SESSION" \
  "$C_RST" "$C_DIM" "$C_BLD" "$C_GRN" "$C_RED" "$C_YEL" "$C_BLU" <<'PY'
import json, sys

path, steps, as_json, session = sys.argv[1], sys.argv[2] == "1", sys.argv[3] == "1", sys.argv[4]
RST, DIM, BLD, GRN, RED, YEL, BLU = sys.argv[5:12]
data = json.load(open(path))


def variables(txn):
    """Flow variables, flattened. Set wins over Get -- it is the value the
    policy actually produced, and a Get of an unset variable is noise."""
    out = {}
    for point in txn.get("point", []) or []:
        for res in point.get("results", []) or []:
            if res.get("ActionResult") != "VariableAccess":
                continue
            for acc in res.get("accessList", []) or []:
                for kind in ("Get", "Set"):
                    v = acc.get(kind)
                    if not v or "name" not in v:
                        continue
                    if kind == "Set" or v["name"] not in out:
                        out[v["name"]] = v.get("value", "")
    return out


def executed(txn):
    """Policy names that actually ran, in order. Read off Execution/DebugInfo:
    a skipped step leaves no Execution point, and step conditions never appear
    as Condition results, so this is the only honest source."""
    seen = []
    for point in txn.get("point", []) or []:
        if point.get("id") != "Execution":
            continue
        for res in point.get("results", []) or []:
            if res.get("ActionResult") != "DebugInfo":
                continue
            for p in (res.get("properties", {}) or {}).get("property", []) or []:
                if p.get("name") == "stepDefinition-name":
                    n = p.get("value", "")
                    if n and n not in seen:
                        seen.append(n)
    return seen


def armor_of(v, ran):
    """Model Armor verdict. filterMatchState is not a documented agw.* flow
    variable, so it is discovered in the trace rather than assumed; falling
    back to whether the sanitize step ran at all."""
    for k, val in v.items():
        if "filtermatchstate" in k.lower():
            return val or "-"
    return "ran" if any("sanitize" in s.lower() for s in ran) else "-"


rows = []
for item in data:
    txn = item.get("txn", {}) or {}
    v = variables(txn)
    ran = executed(txn)
    cache = next((val for k, val in v.items()
                  if k.endswith("cache_hit")), None)
    rows.append({
        "txn": item.get("id", "")[-4:],
        "uri": v.get("request.uri", "-"),
        "model": v.get("agw.model_name") or v.get("agw.requested_model") or "-",
        "bucket": v.get("agw.req_model_bucket", "-"),
        "source": v.get("agw.token_source", "-"),
        "tokens": v.get("agw.total_tokens", "-"),
        "prompt": "set" if v.get("agw.user_prompt") else "-",
        "client": v.get("agw.client_id", "-"),
        "armor": armor_of(v, ran),
        "cache": {"true": "HIT", "false": "miss"}.get(str(cache).lower(), "-"),
        "status": v.get("response.status.code", "-"),
        "steps": ran,
        # The body the CALLER actually receives. verify.md checks 1-9 are all
        # inbound, and that gap shipped a real defect: enforcement verified
        # clean -- 429, counters right, model never called -- while the fault
        # body handed the caller the full principal:// assertion. It sat in
        # three traces unnoticed because nothing put it in front of anyone.
        # So it is printed for refusals, not left one fetch away.
        "body": v.get("response.content", ""),
    })

if as_json:
    print(json.dumps({"session": session, "transactions": rows}, indent=2))
    sys.exit(0)

if not rows:
    # [] is a MEANINGFUL result, and it does NOT prove the callout is dead.
    # Observed on a working proxy: every session on three consecutive
    # revisions returned [] while traffic was demonstrably governed. The
    # AuthzExtension is failOpen, so a dead callout and a healthy one look
    # identical from the client -- which is why the probe, not the empty
    # list, is what settles it.
    print("\n%sNo transactions in session %s.%s" % (BLD, session, RST))
    print("""
This does NOT prove the callout is dead. Corroborate before concluding that:

  Send a prompt the governance layer must refuse -- an injection, if Model
  Armor is on -- and look at the error.

    A 400 carrying errorcode steps.sanitize.user.prompt.FilterMatched proves
    the proxy IS in the path. Only Apigee produces that: the callout lands and
    the tracing is what is broken.

    No refusal, or a generic gateway error, is consistent with a dead callout.

Also check the session had not already expired -- --arm prints the absolute
window, and a PAYG org silently halves a 600s request to 300s.""")
    sys.exit(1)

w = "%s┌─ %s %s%s" % (DIM, "Transactions", "─" * (92 - len("Transactions")), RST)
print(w)
print("  %-5s %-22s %-14s %-7s %-7s %-16s %-5s %s" %
      ("TXN", "MODEL", "BUCKET", "SOURCE", "TOKENS", "ARMOR", "CACHE", "STATUS"))
print("  %-5s %-22s %-14s %-7s %-7s %-16s %-5s %s" %
      ("-" * 5, "-" * 22, "-" * 14, "-" * 7, "-" * 7, "-" * 16, "-" * 5, "-" * 6))
for r in rows:
    colour = GRN if r["status"] in ("200", "-") else YEL
    print("  %-5s %-22s %-14s %-7s %-7s %-16s %-5s %s%s%s" % (
        r["txn"], r["model"][:22], r["bucket"][:14], r["source"], r["tokens"],
        r["armor"][:16], r["cache"], colour, r["status"], RST))

# verify.md check 10: what the CALLER receives on a refusal path. Printed
# unasked for any non-2xx, and scanned for the things that must never appear
# in a body that leaves the proxy.
LEAK_MARKERS = ("principal://", "reasoningEngines/", ".system.id.goog",
                "/projects/", "networkAttachments/")
refusals = [r for r in rows if r["status"] not in ("200", "-") and r["body"]]
if refusals:
    print("\n%s┌─ %s %s%s" % (DIM, "Refusal bodies (what the caller sees)",
                              "─" * (92 - len("Refusal bodies (what the caller sees)")), RST))
    for r in refusals:
        print("  %stxn %s  HTTP %s%s" % (BLD, r["txn"], r["status"], RST))
        body = r["body"]
        print("    " + (body[:600] + " …" if len(body) > 600 else body))
        hits = sorted({m for m in LEAK_MARKERS if m in body})
        if hits:
            print("    %s!! LEAKS %s -- this body reaches whoever called the agent. "
                  "Sanitise it in a fault rule.%s" % (RED, ", ".join(hits), RST))
        else:
            print("    %sno identifier or internal resource name in this body%s" % (GRN, RST))

# The checklist items that are judgements rather than values.
notes = []
for r in rows:
    if r["source"] == "none":
        notes.append("%stxn %s: token_source=none -- the count matched no known shape, "
                     "total_tokens is deliberately unset and the quota will raise "
                     "FailedToResolveTokenUsageCount. Check this before suspecting the quota.%s"
                     % (YEL, r["txn"], RST))
    if r["bucket"] == "other" and "gemini" in r["model"].lower():
        notes.append("%stxn %s: bucket=other on a Gemini turn -- normalization did not find "
                     "the model where it looked.%s" % (YEL, r["txn"], RST))
    if r["prompt"] == "-" and r["armor"] != "-":
        notes.append("%stxn %s: agw.user_prompt unset with Model Armor present -- that is a "
                     "500 per request, not a skipped scan.%s" % (RED, r["txn"], RST))
if len({r["model"] for r in rows if r["model"] != "-"}) > 1 and any(r["cache"] == "HIT" for r in rows):
    notes.append("%sCache HIT with more than one model in this session: the cache key is the "
                 "prompt embedding alone, so verify agw.requested_model matches the shape that "
                 "produced the entry before believing the hit.%s" % (YEL, RST))
if notes:
    print()
    for n in notes:
        print("  " + n)

if steps:
    print("\n%s┌─ %s %s%s" % (DIM, "Steps executed", "─" * (92 - len("Steps executed")), RST))
    for r in rows:
        print("  %stxn %s%s  %s" % (BLD, r["txn"], RST, ", ".join(r["steps"]) or "(none)"))
    print("\n  %sA step absent here was SKIPPED, not failed -- gated steps are expected to "
          "skip on non-model calls.%s" % (DIM, RST))
PY
