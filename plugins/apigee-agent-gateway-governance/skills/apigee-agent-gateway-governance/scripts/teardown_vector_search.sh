#!/bin/bash
# Stop the semantic cache billing, in the order that does not fault traffic.
#
# ensure_vector_search.sh prints these steps on success. That was the whole
# teardown story: a comment in a log the operator has probably scrolled past,
# for the one action that STOPS money being spent and the one with a sharp
# ordering constraint. Standing the index up is --yes gated, resumable,
# cost-disclosed and idempotent; tearing it down was prose. The person doing
# it is also cost-motivated and in a hurry, which is the worst combination for
# a manual ordered procedure.
#
# THE ORDERING IS LOAD-BEARING. SCL-lookup runs continueOnError="false", so
# undeploying the index underneath a live proxy faults EVERY request -- not
# just cache lookups. The proxy has to stop referring to the index before the
# index goes away:
#
#   1. redeploy the proxy without the cache feature, and wait for EXTENSIBLE
#   2. undeploy the index from the endpoint
#
# This script refuses to start step 2 until it has confirmed step 1 landed,
# by reading the deployed revision's bundle back and checking SCL-lookup is
# gone. That check is the reason this is a script and not a runbook.
#
# UNDEPLOY, NEVER DELETE. With no replicas attached the index and endpoint
# cost nothing, and keeping them preserves the ids and the endpoint domain --
# which cannot be derived and has to be read back -- so a rebuild is just the
# deploy step again.
#
# It stops a billing resource, so it applies nothing without --yes.
#
# Data goes to stdout as JSON. Diagnostics go to stderr.

set -euo pipefail

usage() {
  cat <<'EOF'
Tear down the semantic cache's Vector Search deployment, in order.

Usage:
  teardown_vector_search.sh --project P --region R --endpoint EP \
      --deployed-index-id ID --org ORG --env ENV --proxy PROXY [--yes]

Required:
  --project P            project holding the index endpoint
  --region R             region holding the index endpoint
  --endpoint EP          index endpoint id
  --deployed-index-id ID the deployedIndexId to undeploy
  --org ORG              Apigee org, for the step-1 verification
  --env ENV              environment hosting the proxy
  --proxy PROXY          proxy name

Options:
  --skip-proxy-check     undeploy WITHOUT confirming the proxy no longer
                         references the index. Only for an already-deleted
                         proxy; otherwise this is the footgun
  --yes                  actually undeploy
  --help                 this text

Exit status:
  0  undeployed, or dry run
  2  bad invocation, or the proxy still references the index
  3  the undeploy failed
EOF
}

PROJECT=""; REGION=""; ENDPOINT_ID=""; DEPLOYED_ID=""
ORG=""; ENVNAME=""; PROXY=""; APPLY=0; SKIP_PROXY_CHECK=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project) PROJECT="$2"; shift 2 ;;
    --region) REGION="$2"; shift 2 ;;
    --endpoint) ENDPOINT_ID="$2"; shift 2 ;;
    --deployed-index-id) DEPLOYED_ID="$2"; shift 2 ;;
    --org) ORG="$2"; shift 2 ;;
    --env) ENVNAME="$2"; shift 2 ;;
    --proxy) PROXY="$2"; shift 2 ;;
    --skip-proxy-check) SKIP_PROXY_CHECK=1; shift ;;
    --yes) APPLY=1; shift ;;
    --help) usage; exit 0 ;;
    *) usage >&2; echo "unknown argument: $1" >&2; exit 1 ;;
  esac
done

[[ -n "$PROJECT" && -n "$REGION" && -n "$ENDPOINT_ID" && -n "$DEPLOYED_ID" ]] \
  || { usage >&2; exit 2; }
if [[ $SKIP_PROXY_CHECK -eq 0 ]]; then
  [[ -n "$ORG" && -n "$ENVNAME" && -n "$PROXY" ]] \
    || { usage >&2; echo "--org/--env/--proxy are required unless --skip-proxy-check" >&2; exit 2; }
fi

# fd 2: this script logs progress to stderr like the other ensure_*/deploy_*
# scripts, and emits only JSON on stdout.
if [[ -t 2 && -z "${NO_COLOR:-}" && "${TERM:-dumb}" != "dumb" ]]; then
  C_RST=$'\033[0m'; C_DIM=$'\033[2m'; C_BLD=$'\033[1m'
  C_GRN=$'\033[32m'; C_RED=$'\033[31m'; C_YEL=$'\033[33m'; C_BLU=$'\033[36m'
else
  C_RST=; C_DIM=; C_BLD=; C_GRN=; C_RED=; C_YEL=; C_BLU=
fi

log()  { printf '%s\n' "$*" >&2; }
die()  { printf '%s\n' "$*" >&2; exit "${2:-1}"; }
hdr()  { printf '\n%s┌─ %s %s%s\n' "$C_DIM" "$1" "$(printf '─%.0s' $(seq 1 $(( 92 > ${#1} ? 92 - ${#1} : 3 ))))" "$C_RST" >&2; }
row()  { printf '  %s%-8s%s %s\n' "${2:-$C_GRN}" "$1" "$C_RST" "$3" >&2; }
cost() { printf '  %s%s%s\n' "$C_YEL" "$*" "$C_RST" >&2; }

# ------------------------------------------------------- step 1 verified ----
STILL_REFERENCED="unknown"
if [[ $SKIP_PROXY_CHECK -eq 1 ]]; then
  log "==> skipping the proxy check (--skip-proxy-check)"
  STILL_REFERENCED="unchecked"
else
  log "==> confirming the deployed proxy no longer references the index"
  TOKEN="$(gcloud auth application-default print-access-token 2>/dev/null || true)"
  [[ -n "$TOKEN" ]] || die "no ADC token; run: gcloud auth application-default login" 2

  REV="$(curl -s -H "Authorization: Bearer $TOKEN" \
    "https://apigee.googleapis.com/v1/organizations/$ORG/environments/$ENVNAME/deployments" 2>/dev/null \
    | python3 -c '
import json,sys
try: d=json.load(sys.stdin)
except Exception: d={}
print(next((x.get("revision","") for x in d.get("deployments",[]) if x.get("apiProxy")==sys.argv[1]), ""))' "$PROXY" || true)"
  [[ -n "$REV" ]] || die "proxy $PROXY is not deployed in $ENVNAME -- nothing references the index from there; re-run with --skip-proxy-check if that is expected" 2
  log "    deployed revision: $REV"

  BUNDLE="$(mktemp)"; trap 'rm -f "$BUNDLE"' EXIT
  curl -s -H "Authorization: Bearer $TOKEN" \
    "https://apigee.googleapis.com/v1/organizations/$ORG/apis/$PROXY/revisions/$REV?format=bundle" \
    -o "$BUNDLE" 2>/dev/null || true

  if python3 - "$BUNDLE" <<'PY'
import sys, zipfile
try:
    z = zipfile.ZipFile(sys.argv[1])
except Exception:
    sys.exit(2)        # could not read -- treat as "cannot prove it is safe"
hit = any(b"SemanticCacheLookup" in z.read(n) or b"SCL-lookup" in z.read(n)
          for n in z.namelist() if n.endswith(".xml"))
sys.exit(0 if hit else 1)
PY
  then
    STILL_REFERENCED="yes"
    log ""
    log "!! REFUSING. Revision $REV of $PROXY still contains SCL-lookup."
    log "!!"
    log "!! SCL-lookup is continueOnError=\"false\". Undeploying the index"
    log "!! underneath it faults EVERY request through this proxy, not just"
    log "!! cache lookups -- the symptom is a total outage that looks like"
    log "!! Apigee breaking, not like a cache being turned off."
    log "!!"
    log "!! Do step 1 first:"
    log "!!   set semanticCache.enabled:false in your contract file, then"
    log "!!   scripts/deploy_proxy.sh --org $ORG --env $ENVNAME --proxy $PROXY \\"
    log "!!     --template assets/apigee-proxy-template.yaml --yes"
    log "!!   (wait for it to report EXTENSIBLE), then re-run this script."
    die "proxy still references the index; refusing to undeploy" 2
  else
    rc=$?
    [[ $rc -eq 2 ]] && die "could not read revision $REV's bundle to verify it is safe to undeploy. Re-run with --skip-proxy-check only if you are certain the proxy no longer uses the cache." 2
    STILL_REFERENCED="no"
    log "    SCL-lookup is absent from revision $REV -- safe to undeploy"
  fi
fi

# -------------------------------------------------------------- the plan ----
MACHINE="$(gcloud ai index-endpoints describe "$ENDPOINT_ID" --region="$REGION" --project="$PROJECT" \
  --format="value(deployedIndexes.filter(\"id:$DEPLOYED_ID\").extract(\"dedicatedResources.machineSpec.machineType\"))" 2>/dev/null || true)"

hdr "Teardown plan"
row KEEP   "$C_GRN" "index endpoint $ENDPOINT_ID -- undeployed, not deleted"
row KEEP   "$C_GRN" "the index itself -- ids and endpoint domain preserved for a rebuild"
row REMOVE "$C_YEL" "deployed index $DEPLOYED_ID${MACHINE:+ ($MACHINE)} -- this is what bills"
log ""
cost "This STOPS the per-node-hour charge. Nothing else here bills while idle."
cost "Rebuilding later is the deploy step alone (~34 min), not a fresh index."
log ""

if [[ $APPLY -ne 1 ]]; then
  printf '  %sNot applying.%s Re-run with %s--yes%s to undeploy.\n' \
    "$C_BLD" "$C_RST" "$C_BLD" "$C_RST" >&2
  printf '{"changed":false,"reason":"dry run, --yes not given","endpoint":"%s","deployedIndexId":"%s","proxyStillReferences":"%s"}\n' \
    "$ENDPOINT_ID" "$DEPLOYED_ID" "$STILL_REFERENCED"
  exit 0
fi

# ------------------------------------------------------------- step 2 -------
log "==> undeploying $DEPLOYED_ID from $ENDPOINT_ID"
gcloud ai index-endpoints undeploy-index "$ENDPOINT_ID" \
  --deployed-index-id="$DEPLOYED_ID" --region="$REGION" --project="$PROJECT" \
  >/dev/null 2>&1 \
  || die "undeploy failed -- the deployed index is still billing" 3

log "==> verifying no replicas remain"
REMAINING="$(gcloud ai index-endpoints describe "$ENDPOINT_ID" \
  --region="$REGION" --project="$PROJECT" \
  --format='value(deployedIndexes[].id)' 2>/dev/null || true)"
case " $REMAINING " in
  *" $DEPLOYED_ID "*) die "undeploy reported success but $DEPLOYED_ID is still deployed" 3 ;;
esac
log "    remaining deployed indexes: ${REMAINING:-none}"
[[ -z "$REMAINING" ]] && log "    nothing on this endpoint bills now"

printf '{"changed":true,"endpoint":"%s","deployedIndexId":"%s","remainingDeployedIndexes":"%s","proxyStillReferences":"%s"}\n' \
  "$ENDPOINT_ID" "$DEPLOYED_ID" "$REMAINING" "$STILL_REFERENCED"
