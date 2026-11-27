#!/bin/bash
# Stand up the Vertex AI Vector Search index the semantic cache needs, deploy it
# onto an endpoint, and read back the endpoint domain the proxy must dial.
#
# This is the only prerequisite in the skill that BILLS CONTINUOUSLY and the only
# one that takes half an hour. It is billed per node-hour for as long as the
# index is deployed, whether or not any traffic arrives -- not per query.
# Streaming updates add a documented $0.45/GB, negligible at cache scale.
#
# Four things make it worth a script rather than four gcloud commands:
#
#   1. Three index properties are IMMUTABLE and two of them are easy to get
#      wrong: `dimensions` must match the embeddings model's native output
#      width, and `indexUpdateMethod` must be STREAM_UPDATE. Getting either
#      wrong is only discoverable at runtime and only fixable by rebuilding.
#   2. The deploy step takes ~34 minutes (measured 33m44s). Almost the entire
#      cost of a rebuild is that one call, so the script must resume rather
#      than restart.
#   3. The endpoint domain cannot be derived -- its leading label is assigned
#      at creation time and matches no id you already hold. It has to be read
#      back, which is why the proxy template cannot be filled in from the
#      contract file alone.
#   4. Reusing an existing index silently is dangerous: a dimension or update
#      method mismatch has no remedy except a rebuild, which would destroy a
#      populated index. This refuses instead.
#
# Data goes to stdout as JSON. Diagnostics go to stderr.

set -euo pipefail

usage() {
  cat <<'EOF'
Ensure a Vector Search index for the semantic cache feature.

Usage:
  ensure_vector_search.sh --project P --region R --index NAME --endpoint NAME \
      --deployed-index-id ID --embeddings-model MODEL [options]

Required:
  --project P              project holding the index and endpoint
  --region R               must match spec.region and the Apigee instance
  --index NAME             index display name; created if absent, reused if present
  --endpoint NAME          index endpoint display name; created if absent
  --deployed-index-id ID   must equal semanticCache.deployedIndexId in the
                           input file. Lowercase, digits and underscores only.
  --embeddings-model MODEL decides the index width. One of:
                             gemini-embedding-001            3072
                             text-embedding-005               768
                             text-multilingual-embedding-002  768
                             text-embedding-004               768  (serving, but
                                                                    off the
                                                                    supported list)

Options:
  --service-account SA     deployment SA to check for roles/aiplatform.user
  --machine-type TYPE      default e2-standard-2. SHARD_SIZE_SMALL selects this;
                           MEDIUM silently selects e2-standard-16, 8x the
                           machine for a cache holding a handful of entries.
  --timeout SECONDS        wait for the deploy. Default 3600; it normally takes
                           about 34 minutes.
  --yes                    apply. Without it, prints the plan and exits 0.
  --help                   this text

Environment:
  CLOUDSDK_AUTH_ACCESS_TOKEN   set from ADC if unset.

Exit codes:
  0  already correct, or plan shown, or applied successfully
  1  usage error
  2  precondition failed (unknown model, dimension or update-method mismatch,
     deployedIndexId already taken by a different index)
  3  apply failed, or the deployment is still not ready afterwards
EOF
}

log() { printf '%s\n' "$*" >&2; }

# ---------------------------------------------------------------- display ----
# Same palette as assess_integration.sh so the whole skill looks like one tool.
# The tty test is on fd 2, NOT fd 1: every log line here goes to stderr, so
# testing stdout would colour a piped run and leave an interactive one plain --
# exactly backwards. Honours NO_COLOR (no-color.org) and a dumb terminal.
if [[ -t 2 && -z "${NO_COLOR:-}" && "${TERM:-dumb}" != "dumb" ]]; then
  C_RST=$'\033[0m'; C_DIM=$'\033[2m'; C_BLD=$'\033[1m'
  C_GRN=$'\033[32m'; C_RED=$'\033[31m'; C_YEL=$'\033[33m'; C_BLU=$'\033[36m'
else
  C_RST=; C_DIM=; C_BLD=; C_GRN=; C_RED=; C_YEL=; C_BLU=
fi

# hdr <title>           section banner
# row <verb> <text>     a planned change; CREATE/RESERVE cyan, MODIFY yellow
# cost <line>...        standing-spend callout, always yellow
hdr()  { printf '%s\n%s┌─ %s %s%s\n' "" "$C_DIM" "$1" "$(printf '─%.0s' $(seq 1 $(( 92 > ${#1} ? 92 - ${#1} : 3 ))))" "$C_RST" >&2; }
row()  { local c="$C_BLU"; case "$1" in MODIFY|PATCH|APPEND) c="$C_YEL";; REUSE) c="$C_GRN";; esac
         printf '  %s%-8s%s %s\n' "$c" "$1" "$C_RST" "$2" >&2; }
cost() { printf '  %s%s%s\n' "$C_YEL" "$*" "$C_RST" >&2; }

die() { log "ERROR: $1"; exit "${2:-1}"; }

PROJECT=""; REGION=""; INDEX_NAME=""; ENDPOINT_NAME=""; DEPLOYED_ID=""
MODEL=""; SA=""; MACHINE="e2-standard-2"; TIMEOUT=3600; APPLY=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --project) PROJECT="$2"; shift 2 ;;
    --region) REGION="$2"; shift 2 ;;
    --index) INDEX_NAME="$2"; shift 2 ;;
    --endpoint) ENDPOINT_NAME="$2"; shift 2 ;;
    --deployed-index-id) DEPLOYED_ID="$2"; shift 2 ;;
    --embeddings-model) MODEL="$2"; shift 2 ;;
    --service-account) SA="$2"; shift 2 ;;
    --machine-type) MACHINE="$2"; shift 2 ;;
    --timeout) TIMEOUT="$2"; shift 2 ;;
    --yes) APPLY=1; shift ;;
    --help) usage; exit 0 ;;
    *) usage >&2; die "unknown argument: $1" 1 ;;
  esac
done

for v in PROJECT REGION INDEX_NAME ENDPOINT_NAME DEPLOYED_ID MODEL; do
  [[ -n "${!v}" ]] || { usage >&2; die "missing --${v,,}" 1; }
done
[[ "$TIMEOUT" =~ ^[0-9]+$ ]] || die "--timeout must be a whole number of seconds" 1
# deployedIndexId is referenced from the proxy bundle as <DeployedIndexID>; the
# API rejects hyphens and uppercase, and the failure names the field, not the
# rule.
[[ "$DEPLOYED_ID" =~ ^[a-z_][a-z0-9_]*$ ]] \
  || die "--deployed-index-id must be lowercase letters, digits and underscores, starting with a letter or underscore: got '$DEPLOYED_ID'" 1

# The embeddings policy has no dimensionality parameter -- <Embeddings><VertexAI>
# takes a URL and nothing else -- so the model's NATIVE width is what lands in
# the index, and the index width is fixed at creation. That makes this table the
# whole of the compatibility contract.
case "$MODEL" in
  gemini-embedding-001)           DIMS=3072 ;;
  text-embedding-005)             DIMS=768 ;;
  text-multilingual-embedding-002) DIMS=768 ;;
  text-embedding-004)             DIMS=768 ;;
  *) die "unknown --embeddings-model '$MODEL'; pass one of gemini-embedding-001, text-embedding-005, text-multilingual-embedding-002, text-embedding-004, or extend the table in this script after measuring the model's output width" 2 ;;
esac

: "${CLOUDSDK_AUTH_ACCESS_TOKEN:=$(gcloud auth application-default print-access-token 2>/dev/null)}"
export CLOUDSDK_AUTH_ACCESS_TOKEN
[[ -n "$CLOUDSDK_AUTH_ACCESS_TOKEN" ]] \
  || die "could not obtain an ADC token; run 'gcloud auth application-default login'" 2

g=(--region="$REGION" --project="$PROJECT")
id_of() { sed 's|.*/||'; }   # full resource name -> bare numeric id

# Which index is serving under a given deployedIndexId, or empty.
#
# Deliberately NOT gcloud's --format="value(deployedIndexes.filter(...))"
# projection: that silently yields nothing here even when the deployment
# exists, and an empty answer is indistinguishable from "not deployed" -- which
# would send the script off to do a 34-minute billable deploy on top of a
# healthy one. Parse the JSON instead.
deployed_index_for() { # deployed_index_for ENDPOINT_ID DEPLOYED_ID
  gcloud ai index-endpoints describe "$1" "${g[@]}" --format=json 2>/dev/null \
    | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)
for x in d.get('deployedIndexes', []):
    if x.get('id') == '$2':
        print(x.get('index', '').rsplit('/', 1)[-1])
        break
" 2>/dev/null || true
}

# ---------------------------------------------------------------- inspect ----
log "==> inspecting Vector Search in $PROJECT / $REGION"
log "    embeddings model $MODEL -> index must be ${DIMS}-dimensional"

if [[ -n "$SA" ]]; then
  if gcloud projects get-iam-policy "$PROJECT" \
       --flatten="bindings[].members" --format='value(bindings.role)' \
       --filter="bindings.members:serviceAccount:$SA" 2>/dev/null \
       | grep -qx "roles/aiplatform.user"; then
    log "    $SA has roles/aiplatform.user"
  else
    log "    WARNING: $SA does not appear to hold roles/aiplatform.user at the"
    log "             project level. The embeddings and findNeighbors calls run"
    log "             as this account; without it they fail at runtime, not now."
  fi
fi

INDEX_ID="$(gcloud ai indexes list "${g[@]}" \
  --filter="displayName=$INDEX_NAME" --format='value(name)' 2>/dev/null | head -1 | id_of || true)"

index_dims=""; index_method=""
if [[ -n "$INDEX_ID" ]]; then
  index_dims="$(gcloud ai indexes describe "$INDEX_ID" "${g[@]}" \
    --format='value(metadata.config.dimensions)' 2>/dev/null || true)"
  index_method="$(gcloud ai indexes describe "$INDEX_ID" "${g[@]}" \
    --format='value(indexUpdateMethod)' 2>/dev/null || true)"
  log "    index $INDEX_NAME: present ($INDEX_ID), dimensions=${index_dims:-?} method=${index_method:-?}"

  # Both of these are immutable. Rebuilding is the only remedy, and doing it
  # silently would destroy whatever the index already holds.
  if [[ -n "$index_dims" && "$index_dims" != "$DIMS" ]]; then
    die "index '$INDEX_NAME' is ${index_dims}-dimensional but --embeddings-model $MODEL emits $DIMS. Dimensions are fixed at index creation and the SemanticCacheLookup policy cannot truncate, so these cannot be reconciled in config. Either choose a ${index_dims}-dimensional model, or create a new index and change indexId." 2
  fi
  if [[ -n "$index_method" && "$index_method" != "STREAM_UPDATE" ]]; then
    die "index '$INDEX_NAME' has indexUpdateMethod=$index_method. SemanticCachePopulate writes through :upsertDatapoints, which only exists on a STREAM_UPDATE index, and the conversion is closed in both directions. This index can never back the cache; create a streaming one." 2
  fi
else
  log "    index $INDEX_NAME: ABSENT"
fi

ENDPOINT_ID="$(gcloud ai index-endpoints list "${g[@]}" \
  --filter="displayName=$ENDPOINT_NAME" --format='value(name)' 2>/dev/null | head -1 | id_of || true)"

deployed_ok=0; endpoint_domain=""
if [[ -n "$ENDPOINT_ID" ]]; then
  endpoint_domain="$(gcloud ai index-endpoints describe "$ENDPOINT_ID" "${g[@]}" \
    --format='value(publicEndpointDomainName)' 2>/dev/null || true)"
  log "    endpoint $ENDPOINT_NAME: present ($ENDPOINT_ID), domain=${endpoint_domain:-<none yet>}"

  existing_index="$(deployed_index_for "$ENDPOINT_ID" "$DEPLOYED_ID")"
  if [[ -n "$existing_index" ]]; then
    # The id is taken. It is only ours if it serves the very index we resolved;
    # if our index does not exist yet, then by definition it is someone else's.
    if [[ -z "$INDEX_ID" ]]; then
      die "deployedIndexId '$DEPLOYED_ID' on endpoint $ENDPOINT_NAME is already serving index $existing_index, but no index named '$INDEX_NAME' exists -- so this would create a second index and try to deploy it under an id that is already taken. Pick another --deployed-index-id, or point --index at the index that is already deployed." 2
    fi
    if [[ "$existing_index" != "$INDEX_ID" ]]; then
      die "deployedIndexId '$DEPLOYED_ID' on endpoint $ENDPOINT_NAME already serves a different index ($existing_index, not $INDEX_ID). Undeploy it first, or pick another deployedIndexId -- deploying over it is not what you want." 2
    fi
    deployed_ok=1
    log "    deployedIndexId $DEPLOYED_ID: already serving $existing_index"
  else
    log "    deployedIndexId $DEPLOYED_ID: not deployed"
  fi
else
  log "    endpoint $ENDPOINT_NAME: ABSENT"
fi

# ------------------------------------------------------------------- plan ----
plan=()
[[ -z "$INDEX_ID" ]]      && plan+=("create ${DIMS}-dim STREAM_UPDATE index '$INDEX_NAME' (~2 min)")
[[ -z "$ENDPOINT_ID" ]]   && plan+=("create public index endpoint '$ENDPOINT_NAME' (~2 min)")
[[ $deployed_ok -eq 0 ]]  && plan+=("deploy the index as '$DEPLOYED_ID' on $MACHINE, min=max=1 replica (~34 MIN, and STARTS BILLING)")

if [[ ${#plan[@]} -eq 0 ]]; then
  [[ -n "$endpoint_domain" ]] \
    || die "index is deployed but the endpoint reports no publicEndpointDomainName; the proxy cannot be configured without it" 3
  log "==> nothing to do"
  printf '{"changed":false,"indexId":"%s","indexEndpointId":"%s","deployedIndexId":"%s","endpointDomain":"%s","dimensions":%s,"embeddingsModel":"%s"}\n' \
    "$INDEX_ID" "$ENDPOINT_ID" "$DEPLOYED_ID" "$endpoint_domain" "$DIMS" "$MODEL"
  exit 0
fi

hdr "Proposed changes in $PROJECT / $REGION"
for p in "${plan[@]}"; do row CREATE "$p"; done
log ""
cost "COST  a deployed index bills per node-hour for as long as it is deployed,"
cost "      with or without traffic. It is not per-query. One $MACHINE"
cost "      replica runs continuously until you undeploy it, and streaming"
cost "      updates add about \$0.45/GB (negligible at cache scale)."
cost "      This is the only thing in this skill that costs money while idle."
log ""

if [[ $APPLY -eq 0 ]]; then
  printf '  %sNot applying.%s Re-run with %s--yes%s to make these changes.\n' \
    "$C_BLD" "$C_RST" "$C_BLD" "$C_RST" >&2
  printf '{"changed":false,"planned":%d,"indexId":"%s","indexEndpointId":"%s","dimensions":%s}\n' \
    "${#plan[@]}" "$INDEX_ID" "$ENDPOINT_ID" "$DIMS"
  exit 0
fi

# ------------------------------------------------------------------ apply ----
WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT

if [[ -z "$INDEX_ID" ]]; then
  log "==> creating index $INDEX_NAME"
  # No contentsDeltaUri: a cache starts empty. Pointing it at a bucket makes the
  # index try to ingest whatever is there as vector data.
  #
  # indexUpdateMethod is NOT part of this file. --metadata-file supplies the
  # Index resource's `metadata` field, which is validated against the
  # NearestNeighborSearch schema, and that schema defines `config` and nothing
  # else. Putting indexUpdateMethod here fails every create with
  #   "Cannot find field: indexUpdateMethod in message
  #    ...NearestNeighborSearch"
  # It is a top-level field on the Index resource and gcloud exposes it as its
  # own flag, spelled in kebab-case: --index-update-method=stream-update.
  #
  # Do NOT "fix" this by deleting the setting. The flag defaults to
  # BATCH_UPDATE, and SemanticCachePopulate writes through :upsertDatapoints,
  # which only exists on a STREAM_UPDATE index -- the conversion is closed in
  # both directions, so a batch index can never back the cache. The guard at
  # the top of this script would then correctly refuse the index it had just
  # created. The flag must be passed, not dropped.
  cat > "$WORK/index.json" <<JSON
{"config": {"dimensions": $DIMS,
            "approximateNeighborsCount": 10,
            "distanceMeasureType": "DOT_PRODUCT_DISTANCE",
            "shardSize": "SHARD_SIZE_SMALL",
            "algorithm_config": {"treeAhConfig": {}}}}
JSON
  gcloud ai indexes create --display-name="$INDEX_NAME" \
    --metadata-file="$WORK/index.json" \
    --index-update-method=stream-update "${g[@]}" >/dev/null 2>"$WORK/err" \
    || { cat "$WORK/err" >&2; die "index create failed" 3; }
  for _ in $(seq 1 60); do
    INDEX_ID="$(gcloud ai indexes list "${g[@]}" --filter="displayName=$INDEX_NAME" \
      --format='value(name)' 2>/dev/null | head -1 | id_of || true)"
    [[ -n "$INDEX_ID" ]] && break
    sleep 5
  done
  [[ -n "$INDEX_ID" ]] || die "index was created but did not become listable" 3
  log "    created $INDEX_ID"
fi

if [[ -z "$ENDPOINT_ID" ]]; then
  log "==> creating index endpoint $ENDPOINT_NAME"
  gcloud ai index-endpoints create --display-name="$ENDPOINT_NAME" \
    --public-endpoint-enabled "${g[@]}" >/dev/null 2>"$WORK/err" \
    || { cat "$WORK/err" >&2; die "index endpoint create failed" 3; }
  for _ in $(seq 1 60); do
    ENDPOINT_ID="$(gcloud ai index-endpoints list "${g[@]}" --filter="displayName=$ENDPOINT_NAME" \
      --format='value(name)' 2>/dev/null | head -1 | id_of || true)"
    [[ -n "$ENDPOINT_ID" ]] && break
    sleep 5
  done
  [[ -n "$ENDPOINT_ID" ]] || die "index endpoint was created but did not become listable" 3
  log "    created $ENDPOINT_ID"
fi

if [[ $deployed_ok -eq 0 ]]; then
  log "==> deploying index as $DEPLOYED_ID (this takes around 34 minutes)"
  # min=max=1: left unset this can autoscale, and node count is the entire cost
  # of the feature.
  gcloud ai index-endpoints deploy-index "$ENDPOINT_ID" \
    --index="$INDEX_ID" --deployed-index-id="$DEPLOYED_ID" \
    --display-name="$DEPLOYED_ID" --machine-type="$MACHINE" \
    --min-replica-count=1 --max-replica-count=1 \
    "${g[@]}" >/dev/null 2>"$WORK/err" \
    || { cat "$WORK/err" >&2; die "deploy-index failed" 3; }

  deadline=$(( $(date +%s) + TIMEOUT ))
  until [[ -n "$(deployed_index_for "$ENDPOINT_ID" "$DEPLOYED_ID")" ]]; do
    [[ $(date +%s) -ge $deadline ]] \
      && die "deploy did not complete within ${TIMEOUT}s. It may still be running -- re-run this script to pick up where it left off rather than starting over." 3
    sleep 60
    log "    still deploying... ($(( ($(date +%s) - deadline + TIMEOUT) / 60 ))m elapsed)"
  done
  log "    deployed"
fi

# The endpoint domain is assigned at creation and matches no id you hold.
# Read it back; it is what the proxy dials.
endpoint_domain="$(gcloud ai index-endpoints describe "$ENDPOINT_ID" "${g[@]}" \
  --format='value(publicEndpointDomainName)' 2>/dev/null || true)"
[[ -n "$endpoint_domain" ]] \
  || die "endpoint reports no publicEndpointDomainName after deploy; the semantic cache cannot be configured without it" 3

# Cheaper to fail here than as a runtime miss.
final_dims="$(gcloud ai indexes describe "$INDEX_ID" "${g[@]}" \
  --format='value(metadata.config.dimensions)' 2>/dev/null || true)"
[[ "$final_dims" == "$DIMS" ]] \
  || die "index reports ${final_dims:-unknown} dimensions but $MODEL emits $DIMS" 3

log "==> ready"
log "    index            $INDEX_ID (${final_dims}-dim, STREAM_UPDATE)"
log "    endpoint         $ENDPOINT_ID"
log "    deployedIndexId  $DEPLOYED_ID"
log "    endpointDomain   $endpoint_domain"
log ""
log "    TEARDOWN, in this order -- SCL-lookup is continueOnError:false, so"
log "    undeploying underneath a live proxy faults every request:"
log "      1. set semanticCache.enabled:false and redeploy the proxy"
log "      2. gcloud ai index-endpoints undeploy-index $ENDPOINT_ID \\"
log "           --deployed-index-id=$DEPLOYED_ID --region=$REGION --project=$PROJECT"
log "    Undeploy, do not delete: with no replicas attached the index and"
log "    endpoint cost nothing, and keeping them preserves the ids and domain"
log "    so a rebuild is just the deploy step again."

printf '{"changed":true,"indexId":"%s","indexEndpointId":"%s","deployedIndexId":"%s","endpointDomain":"%s","dimensions":%s,"embeddingsModel":"%s","applied":%d}\n' \
  "$INDEX_ID" "$ENDPOINT_ID" "$DEPLOYED_ID" "$endpoint_domain" "$final_dims" "$MODEL" "${#plan[@]}"
