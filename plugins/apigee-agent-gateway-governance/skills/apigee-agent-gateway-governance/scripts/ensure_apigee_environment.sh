#!/bin/bash
# Create the dedicated Apigee environment this proxy needs, attach it to the
# runtime instance in the region, and put it in exactly one envgroup bearing the
# callout hostname.
#
# The environment must be attached to EXACTLY ONE envgroup. In two or more the
# gateway returns 404 for every agent request with the extension never invoked,
# and nothing reports it -- no Apigee error, no debug session, no Cloud
# Monitoring entry. Every later step still succeeds, so nothing downstream
# catches it. That failure is the reason this script exists rather than four
# curl commands in a runbook.
#
# Four things make it worth a script:
#
#   1. Environment creation must NOT send `type`. On a SUBSCRIPTION_2021 org it
#      is rejected outright, and the message blames the pricing plan rather than
#      the request.
#   2. Attaching the environment to the instance takes minutes and LOCKS the
#      environment while it runs. A property PATCH issued in that window fails
#      in a way that looks like a permissions problem.
#   3. An existing envgroup whose hostname differs is NOT reused. Silently
#      repurposing someone else's envgroup would break their routing, and a
#      hostname that does not match the AuthzExtension means the callout never
#      lands and nothing errors.
#   4. The one-envgroup invariant is checked before and after, because an
#      environment that already exists may already be in others.
#
# It creates billable resources, so it applies nothing without --yes.
#
# Data goes to stdout as JSON. Diagnostics go to stderr.

set -euo pipefail

usage() {
  cat <<'EOF'
Ensure a dedicated Apigee environment for the ext-proc proxy.

Usage:
  ensure_apigee_environment.sh --org ORG --env ENV --region R \
      --envgroup GROUP --hostname HOST [options]

Required:
  --org ORG          Apigee organization
  --env ENV          environment to create or verify; must end up dedicated
  --region R         must match the Agent Gateway and the callout endpoint
  --envgroup GROUP   envgroup to create or reuse
  --hostname HOST    callout hostname for the envgroup. Must be byte-identical
                     to the DNS A record and the AuthzExtension authority.

Options:
  --instance NAME    runtime instance to attach to. Default: the single ACTIVE
                     instance in --region; ambiguity is an error, not a guess.
  --timeout SECONDS  how long to wait for the instance attachment.
                     Default 600; it normally takes about four minutes.
  --yes              apply. Without it, prints the plan and exits 0.
  --help             this text

Environment:
  CLOUDSDK_AUTH_ACCESS_TOKEN   set from ADC if unset.

Exit codes:
  0  already correct, or plan shown, or applied successfully
  1  usage error
  2  precondition failed (no instance in region, environment already shared,
     envgroup exists with a different hostname)
  3  apply failed, or the invariant is still violated afterwards
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

ORG=""; ENV=""; REGION=""; ENVGROUP=""; HOSTNAME_=""; INSTANCE=""; TIMEOUT=600; APPLY=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --org) ORG="$2"; shift 2 ;;
    --env) ENV="$2"; shift 2 ;;
    --region) REGION="$2"; shift 2 ;;
    --envgroup) ENVGROUP="$2"; shift 2 ;;
    --hostname) HOSTNAME_="$2"; shift 2 ;;
    --instance) INSTANCE="$2"; shift 2 ;;
    --timeout) TIMEOUT="$2"; shift 2 ;;
    --yes) APPLY=1; shift ;;
    --help) usage; exit 0 ;;
    *) usage >&2; die "unknown argument: $1" 1 ;;
  esac
done

for v in ORG ENV REGION ENVGROUP HOSTNAME_; do
  [[ -n "${!v}" ]] || { usage >&2; die "missing --${v,,}" 1; }
done
[[ "$TIMEOUT" =~ ^[0-9]+$ ]] || die "--timeout must be a whole number of seconds" 1

: "${CLOUDSDK_AUTH_ACCESS_TOKEN:=$(gcloud auth application-default print-access-token 2>/dev/null)}"
export CLOUDSDK_AUTH_ACCESS_TOKEN
[[ -n "$CLOUDSDK_AUTH_ACCESS_TOKEN" ]] \
  || die "could not obtain an ADC token; run 'gcloud auth application-default login'" 2

API="https://apigee.googleapis.com/v1/organizations/$ORG"
auth=(-H "Authorization: Bearer $CLOUDSDK_AUTH_ACCESS_TOKEN")
json=(-H "Content-Type: application/json")

# jq is not assumed; python3 needs only the json stdlib here (no PyYAML).
pyjson() { python3 -c "$1" 2>/dev/null; }

# ---------------------------------------------------------------- inspect ----
log "==> inspecting org $ORG"

# Runtime instance. Guessing the wrong one puts the environment in another
# region, where the callout endpoint cannot reach it.
if [[ -z "$INSTANCE" ]]; then
  mapfile -t candidates < <(curl -sf "${auth[@]}" "$API/instances" 2>/dev/null | pyjson "
import json, sys
for i in json.load(sys.stdin).get('instances', []):
    if i.get('location') == '$REGION' and i.get('state') == 'ACTIVE':
        print(i['name'])
")
  case "${#candidates[@]}" in
    0) die "no ACTIVE runtime instance in $REGION. The environment must attach to an instance in the same region as the gateway." 2 ;;
    1) INSTANCE="${candidates[0]}"; log "    instance: $INSTANCE (only ACTIVE one in $REGION)" ;;
    *) die "$REGION has ${#candidates[@]} ACTIVE instances (${candidates[*]}). Pass --instance to choose." 2 ;;
  esac
else
  log "    instance: $INSTANCE (given)"
fi

env_exists=0
curl -sf "${auth[@]}" "$API/environments/$ENV" >/dev/null 2>&1 && env_exists=1
log "    environment $ENV: $([[ $env_exists -eq 1 ]] && echo present || echo ABSENT)"

instance_attached=0
if [[ $env_exists -eq 1 ]]; then
  if curl -sf "${auth[@]}" "$API/instances/$INSTANCE/attachments" 2>/dev/null | pyjson "
import json, sys
atts = json.load(sys.stdin).get('attachments', [])
sys.exit(0 if any(a.get('environment') == '$ENV' for a in atts) else 1)
"; then instance_attached=1; fi
  log "    attached to $INSTANCE: $([[ $instance_attached -eq 1 ]] && echo yes || echo NO)"
fi

# Envgroup. A hostname mismatch is fatal rather than repaired: the envgroup may
# belong to someone else, and rewriting its hostnames would break their routing.
group_exists=0; group_hostnames=""
if group_json=$(curl -sf "${auth[@]}" "$API/envgroups/$ENVGROUP" 2>/dev/null); then
  group_exists=1
  group_hostnames=$(printf '%s' "$group_json" | pyjson "
import json, sys
print(' '.join(json.load(sys.stdin).get('hostnames', [])))
")
  log "    envgroup $ENVGROUP: present, hostnames: ${group_hostnames:-<none>}"
  if [[ " $group_hostnames " != *" $HOSTNAME_ "* ]]; then
    die "envgroup '$ENVGROUP' already exists with hostnames '$group_hostnames', which does not include '$HOSTNAME_'. Refusing to rewrite an existing envgroup: it may carry other routing, and a hostname that differs from the AuthzExtension authority means the callout never lands and nothing errors. Pick a different --envgroup, or fix the hostname." 2
  fi
else
  log "    envgroup $ENVGROUP: ABSENT"
fi

group_attached=0
if [[ $group_exists -eq 1 ]]; then
  if curl -sf "${auth[@]}" "$API/envgroups/$ENVGROUP/attachments" 2>/dev/null | pyjson "
import json, sys
atts = json.load(sys.stdin).get('environmentGroupAttachments', [])
sys.exit(0 if any(a.get('environment') == '$ENV' for a in atts) else 1)
"; then group_attached=1; fi
fi

# The invariant, checked on what exists today. An environment already sitting in
# other envgroups cannot be made dedicated by adding one more.
count_envgroups() {
  curl -sf "${auth[@]}" "$API/envgroups" 2>/dev/null | pyjson "
import json, sys
print('\n'.join(g['name'] for g in json.load(sys.stdin).get('environmentGroups', [])))
" | while read -r g; do
      [[ -z "$g" ]] && continue
      if curl -sf "${auth[@]}" "$API/envgroups/${g}/attachments" 2>/dev/null | pyjson "
import json, sys
atts = json.load(sys.stdin).get('environmentGroupAttachments', [])
sys.exit(0 if any(a.get('environment') == '$ENV' for a in atts) else 1)
"; then printf '%s ' "$g"; fi
    done
}

existing_groups=""
if [[ $env_exists -eq 1 ]]; then
  existing_groups="$(count_envgroups)"; existing_groups="${existing_groups% }"
  others=""
  for g in $existing_groups; do [[ "$g" != "$ENVGROUP" ]] && others+="$g "; done
  others="${others% }"
  if [[ -n "$others" ]]; then
    die "environment '$ENV' is already attached to envgroup(s) '$others' besides '$ENVGROUP'. A service-extension environment must be in exactly one, or the gateway 404s every agent request with the extension never invoked and no error anywhere. Use a dedicated environment. See references/gotchas.md." 2
  fi
fi

# ------------------------------------------------------------------- plan ----
plan=()
[[ $env_exists -eq 0 ]]        && plan+=("create environment $ENV (without 'type')")
[[ $instance_attached -eq 0 ]] && plan+=("attach $ENV to instance $INSTANCE (minutes; environment is locked meanwhile)")
[[ $group_exists -eq 0 ]]      && plan+=("create envgroup $ENVGROUP with hostname $HOSTNAME_")
[[ $group_attached -eq 0 ]]    && plan+=("attach envgroup $ENVGROUP to $ENV")

if [[ ${#plan[@]} -eq 0 ]]; then
  log "==> nothing to do: $ENV exists, is attached to $INSTANCE, and is in exactly one envgroup ($ENVGROUP)"
  printf '{"changed":false,"environment":"%s","instance":"%s","envgroup":"%s","hostname":"%s"}\n' \
    "$ENV" "$INSTANCE" "$ENVGROUP" "$HOSTNAME_"
  exit 0
fi

hdr "Proposed changes in org $ORG"
for p in "${plan[@]}"; do
  # PATCHing the environment type edits a resource that already exists;
  # everything else here brings something new into being. Colour them apart,
  # because "what are you changing that I already have" is the question.
  case "$p" in
    patch*|*type*COMPREHENSIVE*) row MODIFY "$p" ;;
    *)                          row CREATE "$p" ;;
  esac
done
log ""
cost "These create billable resources. The instance attachment takes about"
cost "four minutes and LOCKS the environment while it runs."
log ""

if [[ $APPLY -eq 0 ]]; then
  printf '  %sNot applying.%s Re-run with %s--yes%s to make these changes.\n' \
    "$C_BLD" "$C_RST" "$C_BLD" "$C_RST" >&2
  printf '{"changed":false,"planned":%d,"environment":"%s","instance":"%s","envgroup":"%s"}\n' \
    "${#plan[@]}" "$ENV" "$INSTANCE" "$ENVGROUP"
  exit 0
fi

# ------------------------------------------------------------------ apply ----
post() { # post URL JSON_BODY ERRLABEL -> response body
  local body code
  body="$(curl -s -w '\n%{http_code}' -X POST "${auth[@]}" "${json[@]}" -d "$2" "$1")"
  code="${body##*$'\n'}"; body="${body%$'\n'*}"
  if [[ "$code" != 2* ]]; then
    log "$3 failed (HTTP $code). Apigee said:"; printf '%s\n' "$body" >&2
    die "$3 failed" 3
  fi
  printf '%s' "$body"
}

# These POSTs return a long-running operation, and the resource is LOCKED until
# it finishes. Critically, the environment is READABLE long before it is ready:
# a GET returns 200 while the create operation is at 1%, so "can I fetch it" is
# not a readiness test. Attaching in that window fails with FAILED_PRECONDITION
# naming the operation that holds the lock. Poll the operation itself.
wait_op() { # wait_op OPERATION_NAME LABEL TIMEOUT_SECONDS
  local op="$1" label="$2" deadline state
  deadline=$(( $(date +%s) + $3 ))
  [[ -n "$op" ]] || die "$label returned no operation to wait on" 3
  while :; do
    state="$(curl -sf "${auth[@]}" "https://apigee.googleapis.com/v1/$op" 2>/dev/null | pyjson "
import json, sys
o = json.load(sys.stdin)
if o.get('error'):
    print('FAILED ' + json.dumps(o['error'].get('message', 'unknown')))
elif o.get('done'):
    print('DONE')
else:
    m = o.get('metadata', {}).get('progress', {})
    print('RUNNING %s' % m.get('percentDone', '?'))
")"
    case "$state" in
      DONE) return 0 ;;
      FAILED*) die "$label failed: ${state#FAILED }" 3 ;;
      *) : ;;
    esac
    [[ $(date +%s) -ge $deadline ]] \
      && die "$label did not finish within $3s. It may still be running; re-run this script to pick up where it left off." 3
    sleep 10
    log "    ${state:-waiting}..."
  done
}

if [[ $env_exists -eq 0 ]]; then
  log "==> creating environment $ENV"
  # No "type" on CREATE: it is rejected on SUBSCRIPTION_2021 orgs with a
  # message about pricing plans. The org default applies instead -- and that
  # default is BASE, which REJECTS extensible proxies. Left alone, the create,
  # the attach and the property PATCH all succeed and only the deploy fails:
  #   "Extensible proxy can not be deployed to a base environment."
  # and it fails AFTER the ~4 minute attachment. Patched below instead, which
  # avoids the create-time rejection and still reaches a usable end state.
  op="$(post "$API/environments" "{\"name\":\"$ENV\"}" "environment create" \
        | pyjson "import json,sys; print(json.load(sys.stdin).get('name',''))")"
  wait_op "$op" "environment create" "$TIMEOUT"
  log "    created"
fi

# --------------------------------------------------------- environment type --
# Unconditional and idempotent: patching an already-COMPREHENSIVE environment
# is a no-op. Done BEFORE the instance attachment so a failure here costs
# seconds instead of arriving four minutes later.
#
# These two calls used a bare $TOKEN, which this script never defines -- every
# other call uses "${auth[@]}". Both sat inside command substitutions ending
# `|| echo ""`, so `set -u` aborted the subshell and the failure was swallowed
# into an empty string; the only tell was `environment type: unknown`, which
# reads as cosmetic. The success log below was also unconditional, so the
# script reported "now COMPREHENSIVE" and exited 0 with applied=4 while the
# environment was still BASE -- surfacing four steps later as a deployment
# that would not come up EXTENSIBLE. Found by a live run.
env_type="$(curl -fsS "${auth[@]}" "$API/environments/$ENV" 2>/dev/null \
            | pyjson "import json,sys; print(json.load(sys.stdin).get('type',''))" || echo "")"

# An empty read is NOT "absent type". A healthy org legitimately omits `type`,
# but so does a failed call, and the two must not be conflated: one is fine to
# patch past, the other means we are flying blind. Probe once more without the
# json filter to tell them apart, and refuse rather than guess.
if [[ -z "$env_type" ]]; then
  if ! curl -fsS "${auth[@]}" "$API/environments/$ENV" >/dev/null 2>&1; then
    die "cannot read environment $ENV to determine its type -- refusing to continue, because a BASE environment that looks unknown will fail at proxy deploy four steps from now"
  fi
  log "==> environment type: not reported (absent is not BASE; patching anyway is a no-op)"
else
  log "==> environment type: $env_type"
fi

if [[ "$env_type" != "COMPREHENSIVE" ]]; then
  log "    BASE cannot host an extensible proxy -- patching to COMPREHENSIVE"
  op="$(curl -fsS -X PATCH "${auth[@]}" \
        -H 'Content-Type: application/json' \
        "$API/environments/$ENV?updateMask=type" \
        -d '{"type":"COMPREHENSIVE"}' \
        | pyjson "import json,sys; print(json.load(sys.stdin).get('name',''))" || echo "")"
  if [[ -n "$op" ]]; then
    wait_op "$op" "environment type patch" "$TIMEOUT"
    log "    now COMPREHENSIVE (apigee-service-extension-enabled survives this)"
  else
    # Never claim success for a call that returned nothing. This is the exact
    # shape of the original defect.
    die "environment type PATCH returned no operation -- $ENV may still be BASE; re-run, or PATCH ?updateMask=type to COMPREHENSIVE by hand before deploying"
  fi
fi

if [[ $instance_attached -eq 0 ]]; then
  log "==> attaching $ENV to instance $INSTANCE (this takes minutes)"
  op="$(post "$API/instances/$INSTANCE/attachments" "{\"environment\":\"$ENV\"}" "instance attach" \
        | pyjson "import json,sys; print(json.load(sys.stdin).get('name',''))")"
  wait_op "$op" "instance attach" "$TIMEOUT"
  log "    attached"
fi

if [[ $group_exists -eq 0 ]]; then
  log "==> creating envgroup $ENVGROUP on $HOSTNAME_"
  post "$API/envgroups" "{\"name\":\"$ENVGROUP\",\"hostnames\":[\"$HOSTNAME_\"]}" "envgroup create" >/dev/null
  log "    created"
fi

if [[ $group_attached -eq 0 ]]; then
  log "==> attaching envgroup $ENVGROUP to $ENV"
  post "$API/envgroups/$ENVGROUP/attachments" "{\"environment\":\"$ENV\"}" "envgroup attach" >/dev/null
  log "    attached"
fi

# ------------------------------------------------------------------ verify ---
log "==> verifying"
final_groups="$(count_envgroups)"; final_groups="${final_groups% }"
final_count=$(wc -w <<<"$final_groups")
[[ "$final_count" -eq 1 && "$final_groups" == "$ENVGROUP" ]] \
  || die "after applying, $ENV is in $final_count envgroup(s) ($final_groups); expected exactly 1 ($ENVGROUP)" 3

curl -sf "${auth[@]}" "$API/instances/$INSTANCE/attachments" 2>/dev/null | pyjson "
import json, sys
atts = json.load(sys.stdin).get('attachments', [])
sys.exit(0 if any(a.get('environment') == '$ENV' for a in atts) else 1)
" || die "after applying, $ENV is not attached to instance $INSTANCE" 3

log "    $ENV is attached to $INSTANCE and is in exactly one envgroup ($ENVGROUP)"
printf '{"changed":true,"environment":"%s","instance":"%s","envgroup":"%s","hostname":"%s","applied":%d}\n' \
  "$ENV" "$INSTANCE" "$ENVGROUP" "$HOSTNAME_" "${#plan[@]}"
