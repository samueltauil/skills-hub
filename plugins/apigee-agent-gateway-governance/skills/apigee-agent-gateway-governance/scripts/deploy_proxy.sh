#!/bin/bash
# Enable a service-extension environment, build the ext-proc proxy from the AFT
# template, deploy it, and confirm it came up EXTENSIBLE.
#
# This sequence is deterministic and order-dependent, and three of its steps
# fail in ways that look like something else:
#   - the environment PATCH replaces the whole properties map
#   - the PATCH is asynchronous, so an immediate readback looks like a failure
#   - the environment is locked while an instance attachment is running
# Encapsulated here so those are handled once rather than re-learned.
#
# Data goes to stdout as JSON. Diagnostics go to stderr.

set -euo pipefail

usage() {
  cat <<'EOF'
Deploy the Apigee Agent Gateway ext-proc proxy.

Usage:
  deploy_proxy.sh --org ORG --env ENV --proxy PROXY --template PATH [options]

Required:
  --org ORG              Apigee organization
  --env ENV              environment that will host the proxy
  --proxy PROXY          proxy name to create or revise
  --template PATH        AFT template; feature files must sit beside it

Options:
  --service-account SA   deployment SA; required if any policy calls a Google
                         API (Model Armor, embeddings, Vector Search), else the
                         deploy is rejected with MISSING_SERVICE_ACCOUNT
  --skip-property        environment property is already set; skip that step
  --yes                  apply. Without it, prints the plan and exits 0.
  --dry-run              explicit form of the default; prints and changes nothing
  --help                 this text

Semantic cache (only if the semanticCache feature is enabled):
  --index-endpoint-id ID Vector Search index endpoint. Its public domain is
                         read back and substituted into the findNeighbors URL;
                         the domain cannot be derived from any id you hold, and
                         the input file has no field for it.
  --index-id ID          Vector Search index, for the upsertDatapoints URL
  --embeddings-model M   with --index-id, refuses to deploy when the index
                         width does not match the model's native output width.
                         A mismatch is only fixable by rebuilding the index.
  --sc-project P         project holding the index endpoint
  --sc-region R          region holding the index endpoint
                         scripts/ensure_vector_search.sh creates all of these
                         and prints the ids as JSON.

Environment:
  CLOUDSDK_AUTH_ACCESS_TOKEN   set automatically from ADC if unset. Needed
                               because under context-aware access the default
                               gcloud credential is rejected with a message
                               that names the resource, not the credential.

Exit codes: 0 ok, 1 usage, 2 precondition failed, 3 deploy not EXTENSIBLE
EOF
}

log() { echo "[$(date +%H:%M:%S)] $*" >&2; }

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

die() { echo "error: $1" >&2; exit "${2:-1}"; }

# Applies nothing without --yes, matching ensure_*/teardown_*. This script
# patches the environment, imports the proxy and deploys a revision, any of
# which can affect live traffic, so the default is plan-only.
ORG=""; ENV=""; PROXY=""; TEMPLATE=""; SA=""; SKIP_PROPERTY=0; DRY_RUN=1; BASE_PATH="/"
INDEX_ENDPOINT_ID=""; INDEX_ID=""; SC_PROJECT=""; SC_REGION=""; EMBEDDINGS_MODEL=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --org) ORG="$2"; shift 2 ;;
    --env) ENV="$2"; shift 2 ;;
    --proxy) PROXY="$2"; shift 2 ;;
    --template) TEMPLATE="$2"; shift 2 ;;
    --service-account) SA="$2"; shift 2 ;;
    --index-endpoint-id) INDEX_ENDPOINT_ID="$2"; shift 2 ;;
    --index-id) INDEX_ID="$2"; shift 2 ;;
    --embeddings-model) EMBEDDINGS_MODEL="$2"; shift 2 ;;
    --sc-project) SC_PROJECT="$2"; shift 2 ;;
    --sc-region) SC_REGION="$2"; shift 2 ;;
    --skip-property) SKIP_PROPERTY=1; shift ;;
    --yes) DRY_RUN=0; shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    --help|-h) usage; exit 0 ;;
    *) usage >&2; die "unknown argument: $1" ;;
  esac
done

[[ -n "$ORG" && -n "$ENV" && -n "$PROXY" && -n "$TEMPLATE" ]] \
  || { usage >&2; die "missing required argument"; }
[[ -f "$TEMPLATE" ]] || die "template not found: $TEMPLATE"
if [[ -n "$INDEX_ENDPOINT_ID" ]]; then
  [[ -n "$SC_PROJECT" && -n "$SC_REGION" ]] \
    || { usage >&2; die "--index-endpoint-id also needs --sc-project and --sc-region (the Vector Search endpoint's own project/region)" 1; }
fi

# Echoes the command in dry-run. Redacts the bearer token: printing it would
# put a live credential into whatever captures stderr.
run() {
  if [[ $DRY_RUN -eq 1 ]]; then
    local shown=()
    for a in "$@"; do
      case "$a" in
        "Authorization: Bearer "*) shown+=("Authorization: Bearer [REDACTED]") ;;
        *) shown+=("$a") ;;
      esac
    done
    printf '  %sDRY-RUN%s %s\n' "$C_BLU" "$C_RST" "${shown[*]}" >&2
    return 0
  fi
  "$@"
}

: "${CLOUDSDK_AUTH_ACCESS_TOKEN:=$(gcloud auth application-default print-access-token 2>/dev/null)}"
export CLOUDSDK_AUTH_ACCESS_TOKEN
[[ -n "$CLOUDSDK_AUTH_ACCESS_TOKEN" ]] || die "could not obtain an ADC token; run 'gcloud auth application-default login'" 2

API="https://apigee.googleapis.com/v1/organizations/$ORG"
auth=(-H "Authorization: Bearer $CLOUDSDK_AUTH_ACCESS_TOKEN")

# 0. Envgroup-count precondition. A service-extension environment must be
# attached to exactly ONE envgroup. In two or more, the gateway 404s every agent
# request with the extension never invoked -- no Apigee error, no debug session,
# no Cloud Monitoring entry. Every other check in this script passes and the
# proxy deploys clean as EXTENSIBLE, so nothing downstream catches it.
#
# This is independent of the base-path check below: an environment can be in two
# envgroups and still have "/" free. Checked first because it is cheap,
# deterministic, and the alternative is bisecting against a known-good setup.
log "counting envgroups attached to $ENV"
envgroup_report=$(
  curl -sf "${auth[@]}" "$API/envgroups" 2>/dev/null \
    | python3 -c '
import json, sys
try:
    groups = [g["name"] for g in json.load(sys.stdin).get("environmentGroups", [])]
except Exception:
    groups = []
print("\n".join(groups))
' 2>/dev/null \
    | while read -r g; do
        [[ -z "$g" ]] && continue
        if curl -sf "${auth[@]}" "$API/envgroups/${g}/attachments" 2>/dev/null \
             | python3 -c "
import json, sys
try:
    atts = json.load(sys.stdin).get('environmentGroupAttachments', [])
except Exception:
    sys.exit(1)
sys.exit(0 if any(a.get('environment') == '$ENV' for a in atts) else 1)
"; then printf '%s ' "$g"; fi
      done
) || true
envgroup_report="${envgroup_report% }"
envgroup_count=$(wc -w <<<"$envgroup_report")

if [[ "$envgroup_count" -eq 1 ]]; then
  log "    $ENV is in exactly one envgroup ($envgroup_report)"
elif [[ "$envgroup_count" -eq 0 ]]; then
  log "    $ENV is in no envgroup yet -- it must end up in exactly one"
else
  die "environment '$ENV' is attached to $envgroup_count envgroups ($envgroup_report). A service-extension environment must be in exactly one, or the gateway returns 404 for every agent request with the extension never invoked and no error reported anywhere. Use a dedicated environment. See references/gotchas.md." 2
fi

# 1. Environment property, preserving every property already set.
if [[ $SKIP_PROPERTY -eq 0 ]]; then
  log "reading existing properties on $ENV"
  existing=$(curl -sf "${auth[@]}" "$API/environments/$ENV") \
    || die "cannot read environment $ENV; check the org and your access" 2

  merged=$(echo "$existing" | python3 -c '
import json, sys
env = json.load(sys.stdin)
props = env.get("properties", {}).get("property", [])
props = [p for p in props if p.get("name") != "apigee-service-extension-enabled"]
props.append({"name": "apigee-service-extension-enabled", "value": "true"})
print(json.dumps({"properties": {"property": props}}))')

  log "setting apigee-service-extension-enabled=true (async; will poll)"
  if [[ $DRY_RUN -eq 0 ]]; then
    resp=$(curl -sf -X PATCH "${auth[@]}" -H 'Content-Type: application/json' \
      "$API/environments/$ENV?updateMask=properties" -d "$merged") \
      || die "property PATCH failed. If it reported FAILED_PRECONDITION with a lock, an instance attachment is still running -- wait for it and retry" 2

    op=$(echo "$resp" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("name",""))')
    if [[ -n "$op" ]]; then
      # Both failure modes here surface LATER as "proxy is not EXTENSIBLE"
      # (exit 3), which sends you to the proxy and the template -- neither of
      # which is the cause. Report them where they happen instead:
      #   1. the operation never finished inside the window
      #   2. the operation finished and FAILED
      op_done=0; op_err=""
      for _ in $(seq 1 60); do
        opjson=$(curl -sf "${auth[@]}" "https://apigee.googleapis.com/v1/$op" || true)
        read -r done_ op_err <<<"$(printf '%s' "$opjson" | python3 -c '
import json, sys
try:
  d = json.load(sys.stdin)
except Exception:
  print("False", ""); raise SystemExit
err = d.get("error") or {}
print(d.get("done", False), (err.get("message") or "").replace("\n", " "))')"
        if [[ "$done_" == "True" ]]; then op_done=1; break; fi
        sleep 5
      done
      [[ -n "$op_err" ]] && die "setting apigee-service-extension-enabled failed: $op_err" 2
      (( op_done )) || die "the property operation did not finish within 5 minutes ($op). The environment property is what makes an extensible proxy deployable, so do not continue -- re-run once it completes." 2
      log "property operation complete"
    fi
  else
    printf '  %sDRY-RUN%s PATCH %s/environments/%s?updateMask=properties\n' \
      "$C_BLU" "$C_RST" "$API" "$ENV" >&2
  fi
fi

# 1a. Semantic cache: index width must match the embeddings model.
#
# The SemanticCacheLookup policy takes only a URL, so the model's native output
# width is what lands in the index, and index width is fixed at creation. A
# mismatch is not a config error you can correct -- the remedy is a full index
# rebuild, and the deploy step alone runs about 34 minutes. Checked here so it
# fails in seconds rather than at runtime against a live agent.
if [[ -n "$INDEX_ID" && -n "$EMBEDDINGS_MODEL" ]]; then
  case "$EMBEDDINGS_MODEL" in
    gemini-embedding-001)            want_dims=3072 ;;
    text-embedding-005)              want_dims=768 ;;
    text-multilingual-embedding-002) want_dims=768 ;;
    text-embedding-004)              want_dims=768 ;;
    *) die "unknown --embeddings-model '$EMBEDDINGS_MODEL'; extend the width table in this script and in scripts/ensure_vector_search.sh after measuring the model's output width" 2 ;;
  esac
  log "checking index $INDEX_ID is ${want_dims}-dimensional for $EMBEDDINGS_MODEL"
  have_dims="$(gcloud ai indexes describe "$INDEX_ID" \
    --region="$SC_REGION" --project="$SC_PROJECT" \
    --format='value(metadata.config.dimensions)' 2>/dev/null || true)"
  [[ -n "$have_dims" ]] \
    || die "cannot read dimensions for index $INDEX_ID in $SC_PROJECT/$SC_REGION; check --index-id, --sc-project and --sc-region" 2
  [[ "$have_dims" == "$want_dims" ]] \
    || die "index $INDEX_ID is ${have_dims}-dimensional but --embeddings-model $EMBEDDINGS_MODEL emits $want_dims. Dimensions are fixed at index creation and the policy cannot truncate, so this cannot be reconciled in config -- pick a ${have_dims}-dimensional model, or build a new index (scripts/ensure_vector_search.sh)." 2
  log "    dimensions match ($have_dims)"
fi

# 1a-bis. The REVERSE of the leftover-placeholder check further down.
#
# That one catches a placeholder that survived substitution. This one catches
# a placeholder that was never there -- i.e. someone pasted concrete ids into
# the shipped feature file instead of passing the flags. That deploys
# correctly, so nothing else notices, but it bakes one deployment's ids into a
# file meant to be reusable and skips the substitution check rather than
# exercising it. A warning, not a refusal: a deliberate fork is legitimate,
# and failing a working deploy over file hygiene would be worse than the
# problem.
SRC_CACHE="$(dirname "$TEMPLATE")/feature-semantic-cache.yaml"
if [[ -e "$SRC_CACHE" ]]; then
  SUBSTITUTED=""
  for tok in INDEX_ENDPOINT_DOMAIN INDEX_ENDPOINT_ID INDEX_ID; do
    grep -q "\b$tok\b" "$SRC_CACHE" || SUBSTITUTED="$SUBSTITUTED $tok"
  done
  if [[ -n "$SUBSTITUTED" ]]; then
    log "!! WARNING: feature-semantic-cache.yaml has no$SUBSTITUTED placeholder."
    log "!!          It looks hand-substituted. Concrete ids in a shipped asset"
    log "!!          are not reusable across deployments, and the"
    log "!!          leftover-placeholder check below cannot verify what it"
    log "!!          cannot see. Prefer: git checkout the feature file and pass"
    log "!!          --index-endpoint-id / --index-id / --sc-project / --sc-region."
  fi
fi

# 1b. Semantic cache: resolve the index endpoint domain and substitute it.
#
# The findNeighbors host is the index endpoint's OWN domain, and its leading
# label is assigned at endpoint-creation time -- it matches neither the index
# id, the endpoint id, nor the project number, so it cannot be derived and the
# input file has no field for it. It has to be read back. Without this, a user
# who filled in every documented field still cannot compile a working cache.
if [[ -n "$INDEX_ENDPOINT_ID" ]]; then
  log "resolving index endpoint domain for $INDEX_ENDPOINT_ID"
  ENDPOINT_DOMAIN="$(gcloud ai index-endpoints describe "$INDEX_ENDPOINT_ID" \
    --region="$SC_REGION" --project="$SC_PROJECT" \
    --format='value(publicEndpointDomainName)' 2>/dev/null || true)"
  [[ -n "$ENDPOINT_DOMAIN" ]] \
    || die "index endpoint $INDEX_ENDPOINT_ID reports no publicEndpointDomainName. It must be created with --public-endpoint-enabled and have an index deployed; scripts/ensure_vector_search.sh does both." 2
  log "    $ENDPOINT_DOMAIN"

  # Work on a copy: substituting in place would edit the shipped assets.
  SUBST_DIR="$(mktemp -d)"; trap 'rm -rf "$SUBST_DIR"' EXIT
  cp "$(dirname "$TEMPLATE")"/*.yaml "$SUBST_DIR"/ 2>/dev/null || true
  TEMPLATE="$SUBST_DIR/$(basename "$TEMPLATE")"

  # WORD BOUNDARIES ARE LOAD-BEARING. DEPLOYED_INDEX_ID *contains* INDEX_ID, so
  # a plain s/INDEX_ID/.../g rewrites the parameter's own name:
  #     - name: DEPLOYED_INDEX_ID   ->   - name: DEPLOYED_3873425533026959360
  # and rewrites its reference to match, so the bundle still compiles and still
  # works -- the breakage only surfaces later, when the template tries to
  # supply a DEPLOYED_INDEX_ID that no longer exists. Same shape for
  # INDEX_ENDPOINT_ID against INDEX_ENDPOINT_DOMAIN.
  for f in "$SUBST_DIR"/*.yaml; do
    [[ -e "$f" ]] || continue
    # Longest first as a second line of defence; \b is what actually does it.
    sed -i \
      -e "s|\bINDEX_ENDPOINT_DOMAIN\b|$ENDPOINT_DOMAIN|g" \
      -e "s|\bINDEX_ENDPOINT_ID\b|$INDEX_ENDPOINT_ID|g" \
      ${INDEX_ID:+-e "s|\bINDEX_ID\b|$INDEX_ID|g"} \
      -e "s|\bPROJECT\b|$SC_PROJECT|g" \
      -e "s|\bREGION\b|$SC_REGION|g" \
      "$f"
  done

  # Assert nothing survived. A leftover placeholder compiles fine and fails at
  # runtime against a hostname that does not resolve.
  if leftovers=$(grep -l -E '\b(INDEX_ENDPOINT_DOMAIN|INDEX_ENDPOINT_ID|INDEX_ID)\b' "$SUBST_DIR"/*.yaml 2>/dev/null); then
    log "placeholders survived substitution in:"; printf '%s\n' "$leftovers" >&2
    die "substitution incomplete -- refusing to import a half-substituted bundle" 2
  fi
  # And that the trap did not fire: the parameter must still be named.
  if grep -q 'DEPLOYED_INDEX_ID' "$SUBST_DIR"/feature-semantic-cache.yaml 2>/dev/null; then
    log "    DEPLOYED_INDEX_ID intact; substitution did not corrupt it"
  elif [[ -e "$SUBST_DIR/feature-semantic-cache.yaml" ]]; then
    die "substitution corrupted the DEPLOYED_INDEX_ID parameter name -- this is the INDEX_ID substring trap. Do not import this bundle." 2
  fi
fi

# 1c. Model Armor's template name has its own placeholders, and they are NOT
# covered by the semantic-cache substitution above -- that whole block only
# runs when --index-endpoint-id is passed. Model Armor needs no flag on this
# script, so an unsubstituted MA_TEMPLATE_NAME would otherwise import and
# deploy clean and then fail every matching request at runtime, which is the
# worst failure shape this skill has: fail-closed, on live traffic, with
# nothing wrong at deploy time.
#
# Checked against the bundle actually being imported, whatever produced it.
# The anchored pattern matters: the shipped template lists the optional
# features as COMMENTED examples, so a plain substring match fires on the
# default bundle and blocks a deploy that has no Model Armor in it at all.
# Match an actual list entry only.
MA_FILE="$(dirname "$TEMPLATE")/feature-model-armor.yaml"
if [[ -e "$MA_FILE" ]] && grep -qE '^[[:space:]]*-[[:space:]]*feature-model-armor\.yaml' "$TEMPLATE"; then
  if ma_left=$(grep -nE '\b(MA_TEMPLATE|PROJECT|REGION)\b' "$MA_FILE"); then
    log "Model Armor is enabled but its template name still carries placeholders:"
    printf '%s\n' "$ma_left" >&2
    log "    substitute projects/PROJECT/locations/REGION/templates/MA_TEMPLATE"
    log "    with your real Model Armor template, or drop feature-model-armor.yaml"
    log "    from the template's features list."
    die "refusing to deploy Model Armor with an unresolved template name" 2
  fi
  log "    Model Armor template name substituted"
fi

# 2. Build from the template. GA carries --from-template as of gcloud 588.0.0.
log "importing $PROXY from $TEMPLATE"
if [[ $DRY_RUN -eq 1 ]]; then
  printf '  %sDRY-RUN%s gcloud apigee apis import organizations/%s/apis/%s --from-template=%s\n' \
    "$C_BLU" "$C_RST" "$ORG" "$PROXY" "$TEMPLATE" >&2
  REV="DRY-RUN"
else
  out=$(gcloud apigee apis import "organizations/$ORG/apis/$PROXY" \
        --from-template="$TEMPLATE" 2>&1) \
    || die "import failed. Needs gcloud >= 588.0.0 for --from-template on GA. Output: $out" 2
  REV=$(echo "$out" | sed -n "s/^revision: '\{0,1\}\([0-9]*\)'\{0,1\}/\1/p" | tail -1)
  [[ -n "$REV" ]] || die "import succeeded but no revision was returned: $out" 2
  log "imported revision $REV"
fi

# 2b. Base-path conflict pre-check. Apigee allows one proxy per base path per
# environment, and the failure arrives only at deploy time -- after the import
# has already left an undeployed revision behind. Enumerate first and name the
# offender.
if [[ $DRY_RUN -eq 0 ]]; then
  log "checking base paths already taken in $ENV"
  conflict="$(curl -s "${auth[@]}" "$API/environments/$ENV/deployments" 2>/dev/null | python3 -c "
import json, sys, urllib.request, os
want = '$BASE_PATH'
proxy = '$PROXY'
try:
    deps = json.load(sys.stdin).get('deployments', [])
except Exception:
    sys.exit(0)
tok = os.environ['CLOUDSDK_AUTH_ACCESS_TOKEN']
api = '$API'
for d in deps:
    name, rev = d.get('apiProxy'), d.get('revision')
    if name == proxy:
        continue
    req = urllib.request.Request(f'{api}/apis/{name}/revisions/{rev}',
                                 headers={'Authorization': f'Bearer {tok}'})
    try:
        body = json.load(urllib.request.urlopen(req, timeout=15))
    except Exception:
        continue
    for bp in body.get('basepaths', []):
        if bp == want:
            print(f'{name} revision {rev}')
            sys.exit(0)
" 2>/dev/null || true)"
  if [[ -n "$conflict" ]]; then
    die "base path '$BASE_PATH' in environment '$ENV' is already taken by $conflict. '$ENV' is carrying other traffic, so it is not the dedicated environment this proxy needs -- a shared environment also causes the 404-with-no-error failure described in references/gotchas.md. Move this proxy to a dedicated environment rather than freeing the path." 2
  fi
  log "    base path $BASE_PATH is free"
fi

# 3. Deploy.
deploy_url="$API/environments/$ENV/apis/$PROXY/revisions/$REV/deployments?override=true"
[[ -n "$SA" ]] && deploy_url="$deploy_url&serviceAccount=$SA"
log "deploying revision $REV"
if [[ $DRY_RUN -eq 0 ]]; then
  # No -f: -f discards the body, and the body is where the real cause lives.
  # A CONFLICTING_DEPLOYMENT was once reported as a service-account problem
  # purely because the response was thrown away.
  deploy_body="$(curl -s -w '\n%{http_code}' -X POST "${auth[@]}" "$deploy_url")"
  deploy_code="${deploy_body##*$'\n'}"; deploy_body="${deploy_body%$'\n'*}"
  if [[ "$deploy_code" != 2* ]]; then
    log "deploy failed (HTTP $deploy_code). Apigee said:"
    printf '%s\n' "$deploy_body" >&2
    case "$deploy_body" in
      *CONFLICTING_DEPLOYMENT*)
        die "another proxy already occupies this base path in $ENV, so $ENV is not a dedicated environment; move this proxy to one of its own" 2 ;;
      *MISSING_SERVICE_ACCOUNT*)
        die "pass --service-account: a policy in this proxy calls a Google API" 2 ;;
      *) die "deploy failed" 2 ;;
    esac
  fi
else
  run curl -s -X POST "${auth[@]}" "$deploy_url" >/dev/null
fi

# 4. Confirm EXTENSIBLE. STANDARD means it will not see off-Apigee egress.
if [[ $DRY_RUN -eq 1 ]]; then
  printf '  %sNot applying.%s Re-run with %s--yes%s to make these changes.\n' \
    "$C_BLD" "$C_RST" "$C_BLD" "$C_RST" >&2
  echo '{"dryRun": true, "changed": false, "reason": "dry run, --yes not given"}'
  exit 0
fi

log "waiting for the deployment to report its type"
for _ in $(seq 1 20); do
  state=$(curl -sf "${auth[@]}" "$API/environments/$ENV/deployments" \
    | python3 -c "
import json, sys
for d in json.load(sys.stdin).get('deployments', []):
    if d.get('apiProxy') == '$PROXY' and d.get('revision') == '$REV':
        print(d.get('proxyDeploymentType', '')); break
" 2>/dev/null || true)
  [[ -n "$state" ]] && break
  sleep 5
done

# The deployment type is the whole verdict: STANDARD deploys clean and governs
# nothing, so it must not be just another field in a JSON blob.
hdr "Deployment result"
if [[ "$state" == "EXTENSIBLE" ]]; then
  printf '  %s%-12s%s %s rev %s on %s\n' "$C_GRN" "EXTENSIBLE" "$C_RST" "$PROXY" "$REV" "$ENV" >&2
  printf '  %sThe gateway can call this proxy.%s\n' "$C_DIM" "$C_RST" >&2
else
  printf '  %s%-12s%s %s rev %s on %s\n' "$C_RED" "${state:-UNKNOWN}" "$C_RST" "$PROXY" "$REV" "$ENV" >&2
  printf '  %sNOT EXTENSIBLE -- the callout will never be invoked. The proxy is\n  deployed and healthy and governs nothing. Check that the environment\n  carries apigee-service-extension-enabled=true and is COMPREHENSIVE.%s\n' \
    "$C_RED" "$C_RST" >&2
fi

python3 -c "
import json
print(json.dumps({'org': '$ORG', 'environment': '$ENV', 'proxy': '$PROXY',
                  'revision': '$REV', 'proxyDeploymentType': '$state'}, indent=2))"

if [[ "$state" != "EXTENSIBLE" ]]; then
  echo "error: deployed as '${state:-unknown}', not EXTENSIBLE. The proxy will not" >&2
  echo "       see the agent's off-Apigee tool egress. Check that the environment" >&2
  echo "       property is set and that the proxy is genuinely no-route." >&2
  exit 3
fi
log "EXTENSIBLE confirmed"
