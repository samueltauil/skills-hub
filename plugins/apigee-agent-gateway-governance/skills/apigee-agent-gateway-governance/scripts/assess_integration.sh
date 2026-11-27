#!/bin/bash
# Read the live state of an Agent Gateway + Apigee ext-proc setup and report it.
#
# Strictly READ-ONLY. It creates, modifies and deletes nothing, so it is safe to
# run against production and safe to run before the user has agreed to anything.
#
# Two callers, one discovery pass:
#   - "assess"  -- answer "how is this running, and what is wrong with it"
#   - the PLAN  -- decide CREATE vs REUSE per resource before a dev-mode run,
#                  which is the only honest way to say what is shared with an
#                  existing deployment (another governance extension, say)
#                  rather than guessed
#
# Every check that can fail silently in this stack has an entry here. That is
# the point: nothing below reports a problem at runtime on its own.
#
# Data goes to stdout as JSON with --json. The table goes to stdout otherwise.
# Diagnostics go to stderr.

set -euo pipefail

usage() {
  cat <<'EOF'
Assess an Agent Gateway + Apigee ext-proc setup. Read-only.

Usage:
  assess_integration.sh --project P --region R --gateway G [options]

Required:
  --project P            GCP project
  --region R             region; the gateway, the subnet and the Apigee
                         instance must all share it
  --gateway G            Agent Gateway name

Options:
  --org ORG              Apigee org (default: --project)
  --env ENV              environment expected to host the proxy
  --envgroup EG          environment group expected to carry the hostname
  --hostname H           callout hostname; must match the DNS record and the
                         AuthzExtension authority byte for byte
  --proxy PROXY          proxy name
  --vpc VPC              VPC the gateway egresses into
  --subnet SUBNET        subnet the PSC endpoint is reserved in
  --json                 machine-readable; the plan reads this
  --help                 this text

Exit status:
  0  no FAILs (WARNs may be present)
  1  at least one FAIL
  2  bad invocation
EOF
}

PROJECT=""; REGION=""; GATEWAY=""; ORG=""; ENVNAME=""; ENVGROUP=""
HOSTNAME_=""; PROXY=""; VPC=""; SUBNET=""; JSON=0

# How this script recognises resources THIS skill created, as opposed to some
# other extension on the same gateway. Defined once: these used to be the bare
# string "extproc" scattered across three places, and renaming the resources
# silently broke every one of them.
readonly OUR_POLICY_MATCH="apigee-governance"       # <gateway>-apigee-governance-policy
readonly OUR_PSC_MATCH="agent-gateway-callout-psc"  # agent-gateway-callout-psc-endpoint

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project)  PROJECT="$2"; shift 2 ;;
    --region)   REGION="$2"; shift 2 ;;
    --gateway)  GATEWAY="$2"; shift 2 ;;
    --org)      ORG="$2"; shift 2 ;;
    --env)      ENVNAME="$2"; shift 2 ;;
    --envgroup) ENVGROUP="$2"; shift 2 ;;
    --hostname) HOSTNAME_="$2"; shift 2 ;;
    --proxy)    PROXY="$2"; shift 2 ;;
    --vpc)      VPC="$2"; shift 2 ;;
    --subnet)   SUBNET="$2"; shift 2 ;;
    --json)     JSON=1; shift ;;
    --help)     usage; exit 0 ;;
    *) echo "unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done

[[ -n "$PROJECT" && -n "$REGION" && -n "$GATEWAY" ]] || { usage >&2; exit 2; }
ORG="${ORG:-$PROJECT}"

# Apply the skill's own documented defaults for anything not passed, and
# remember which ones were assumed.
#
# These sections used to be guarded on the flag being set, so a bare
# `--project --region --gateway` invocation silently skipped the entire Apigee
# half -- environment, envgroup, proxy, PSC and DNS -- and still printed a
# confident Setup Status Summary over the six checks that did run. Six
# categories reported "missing" that had never been looked at. Defaulting to
# the documented layout means the common invocation assesses the whole thing,
# and ASSUMED records what was inferred rather than supplied, so the output can
# say so instead of implying it was told.
ASSUMED=()
[[ -z "$ENVNAME"   ]] && { ENVNAME="agent-gateway-govern";                      ASSUMED+=("env=$ENVNAME"); }
[[ -z "$ENVGROUP"  ]] && { ENVGROUP="agent-gateway-govern-group";               ASSUMED+=("envgroup=$ENVGROUP"); }
[[ -z "$PROXY"     ]] && { PROXY="agent-gateway-governance";                    ASSUMED+=("proxy=$PROXY"); }
[[ -z "$HOSTNAME_" ]] && { HOSTNAME_="agent-gateway-callout.internal.${PROJECT}.local"; ASSUMED+=("hostname=$HOSTNAME_"); }

PASS=0; FAILN=0; WARN=0; TODO=0; SKIPN=0
ROWS=()

# Colour. Disabled when stdout is not a tty, when NO_COLOR is set (no-color.org),
# or under --json, so piped and captured output stays plain text.
#
# The tty test here is on fd 1, and in the four ensure_*/deploy_* scripts it is
# on fd 2. That is deliberate, not drift: this script prints its tables to
# STDOUT (they are the product, and --json replaces them), while the others log
# progress to STDERR. Each tests the stream it actually writes to. Normalising
# the two would colour a piped run and leave an interactive one plain in
# whichever script got the wrong fd.
if [[ -t 1 && -z "${NO_COLOR:-}" && "${TERM:-dumb}" != "dumb" ]]; then
  C_RST=$'\033[0m'; C_DIM=$'\033[2m'; C_BLD=$'\033[1m'
  C_GRN=$'\033[32m'; C_RED=$'\033[31m'; C_YEL=$'\033[33m'; C_BLU=$'\033[36m'
else
  C_RST=; C_DIM=; C_BLD=; C_GRN=; C_RED=; C_YEL=; C_BLU=
fi

# hdr <title> -- byte-identical to the helper in the four ensure_*/deploy_*
# scripts, so a header looks the same wherever it is printed. Writes to stdout
# here because this script's output IS stdout; the others write theirs to
# stderr. Rule fills to a fixed 92 columns in both.
hdr() { printf '\n%s┌─ %s %s%s\n' "$C_DIM" "$1" "$(printf '─%.0s' $(seq 1 $(( 92 > ${#1} ? 92 - ${#1} : 3 ))))" "$C_RST"; }

# paint <status> -> the status word, coloured and padded to 6.
paint() {
  case "$1" in
    PASS) printf '%s%-6s%s' "$C_GRN" "PASS" "$C_RST" ;;
    FAIL) printf '%s%-6s%s' "$C_RED" "FAIL" "$C_RST" ;;
    WARN) printf '%s%-6s%s' "$C_YEL" "WARN" "$C_RST" ;;
    TODO) printf '%s%-6s%s' "$C_BLU" "TODO" "$C_RST" ;;
    SKIP) printf '%s%-6s%s' "$C_DIM" "SKIP" "$C_RST" ;;
    *)    printf '%-6s' "$1" ;;
  esac
}

# record <status> <resource> <detail>
#
# Four statuses, and the TODO/FAIL split is the load-bearing one. TODO means
# "this skill creates it and has not yet" -- absence is the expected state of a
# greenfield project, not a defect. FAIL means something is actually wrong:
# a user prerequisite missing, or a conflict no build step will resolve.
# Reporting a never-built setup as a wall of FAIL reads as breakage and is the
# single most misleading thing this script used to do.
record() {
  local st="$1" res="$2" det="$3"
  case "$st" in
    PASS) PASS=$((PASS+1)) ;;
    FAIL) FAILN=$((FAILN+1)) ;;
    WARN) WARN=$((WARN+1)) ;;
    TODO) TODO=$((TODO+1)) ;;
    SKIP) SKIPN=$((SKIPN+1)) ;;
  esac
  ROWS+=("$st|$res|$det")
}

api() {  # api <url> -> body on stdout, empty on failure
  curl -s -H "Authorization: Bearer ${TOKEN}" "$1" 2>/dev/null || true
}

jqf() {  # jqf <json> <python-expr over d> -- no jq dependency
  python3 -c '
import json,sys
try: d=json.loads(sys.stdin.read() or "{}")
except Exception: d={}
try: print(eval(sys.argv[1]))
except Exception: print("")
' "$1" 2>/dev/null || true
}

# ---------------------------------------------------------------- toolchain --
GCV="$(gcloud version 2>/dev/null | sed -n 's/^Google Cloud SDK //p' | head -1)"
if [[ -z "$GCV" ]]; then
  record FAIL "gcloud" "not on PATH"
else
  MAJOR="${GCV%%.*}"
  # 588.0.0 is where `apis import --from-template` reached the GA track. Below
  # it the GA command rejects the flag with an error that reads like the
  # command does not exist, and `gcloud beta` is the fallback. This check used
  # to say 585, which disagreed with every other statement of the minimum in
  # this skill and would have passed an SDK the build then failed on.
  if (( MAJOR < 588 )); then
    record WARN "gcloud" "$GCV -- below 588.0.0; 'apis import --from-template' is GA only from 588, use 'gcloud beta' or upgrade"
  else
    record PASS "gcloud" "$GCV"
  fi
fi

TOKEN="$(gcloud auth application-default print-access-token 2>/dev/null || true)"
if [[ -z "$TOKEN" ]]; then
  record FAIL "credentials" "no ADC token; run gcloud auth application-default login"
else
  record PASS "credentials" "ADC token present"
fi

# ------------------------------------------------------------------ gateway --
GW="$(gcloud network-services agent-gateways describe "$GATEWAY" \
      --location="$REGION" --project="$PROJECT" --format=json 2>/dev/null || true)"
if [[ -z "$GW" ]]; then
  record FAIL "agentGateway/$GATEWAY" "not found in $REGION"
else
  record PASS "agentGateway/$GATEWAY" "exists"
  GAP="$(jqf 'd.get("googleManaged",{}).get("governedAccessPath","")' <<<"$GW")"
  if [[ "$GAP" == "AGENT_TO_ANYWHERE" ]]; then
    record PASS "  governedAccessPath" "$GAP"
  else
    record WARN "  governedAccessPath" "${GAP:-unset} -- egress governance expects AGENT_TO_ANYWHERE"
  fi

  NA="$(jqf 'd.get("networkConfig",{}).get("egress",{}).get("networkAttachment","")' <<<"$GW")"
  if [[ -n "$NA" ]]; then
    record PASS "  egress.networkAttachment" "${NA##*/}  (REUSE: a route into the VPC, not to a service)"
  else
    record TODO "  egress.networkAttachment" "absent -- ensure_gateway_connectivity.sh attaches it; until then the callout has no route into the VPC"
  fi

  DOMS="$(jqf '",".join(d.get("networkConfig",{}).get("dnsPeeringConfig",{}).get("domains",[]))' <<<"$GW")"
  if [[ -n "$DOMS" ]]; then
    if [[ -n "$HOSTNAME_" && "$DOMS" != *"${HOSTNAME_#*.}"* ]]; then
      record WARN "  dnsPeeringConfig" "$DOMS -- does not cover ${HOSTNAME_#*.}; APPEND a second domain, peering is per-domain"
    else
      record PASS "  dnsPeeringConfig" "$DOMS"
    fi
  else
    record TODO "  dnsPeeringConfig" "absent -- ensure_gateway_connectivity.sh appends the domain; until then the host does not resolve"
  fi

  SESA="$(jqf 'd.get("agentGatewayCard",{}).get("serviceExtensionsServiceAccount","")' <<<"$GW")"
  [[ -n "$SESA" ]] && record PASS "  serviceExtensionsSA" "$SESA"
fi

# --------------------------------------------------------- authz policies ----
POLS="$(gcloud beta network-security authz-policies list --location="$REGION" \
        --project="$PROJECT" --format='value(name)' 2>/dev/null || true)"
OURS=""; OUR_SUF=""; OTHER_CONTENT=0
while read -r p; do
  [[ -z "$p" ]] && continue
  PD="$(gcloud beta network-security authz-policies describe "${p##*/}" \
        --location="$REGION" --project="$PROJECT" --format=json 2>/dev/null || true)"
  TGT="$(jqf '",".join(r for r in d.get("target",{}).get("resources",[]))' <<<"$PD")"
  [[ "$TGT" != *"/agentGateways/$GATEWAY"* ]] && continue
  PROF="$(jqf 'd.get("policyProfile","")' <<<"$PD")"
  SUF="$(jqf '",".join(s.get("suffix","") for r in d.get("httpRules",[]) for o in r.get("to",{}).get("operations",[]) for s in o.get("paths",[]))' <<<"$PD")"
  # Semantic match first: does this policy's extension front OUR hostname?
  MINE=0
  if [[ "${p##*/}" == *"$OUR_POLICY_MATCH"* ]]; then
    MINE=1
  elif [[ "$PROF" == "CONTENT_AUTHZ" && -n "$HOSTNAME_" ]]; then
    EXTR="$(jqf '",".join(d.get("customProvider",{}).get("authzExtension",{}).get("resources",[]))' <<<"$PD")"
    if [[ -n "$EXTR" ]]; then
      EXTSVC="$(gcloud service-extensions authz-extensions describe "${EXTR##*/}" \
                --location="$REGION" --project="$PROJECT" --format='value(service)' 2>/dev/null || true)"
      [[ "$EXTSVC" == "$HOSTNAME_" ]] && MINE=1
    fi
  fi
  if (( MINE )); then
    OURS="${p##*/}"; OUR_SUF="$SUF"
    record PASS "authzPolicy/${p##*/}" "$PROF  suffixes=[${SUF}]"
  elif [[ "$PROF" == "CONTENT_AUTHZ" ]]; then
    OTHER_CONTENT=$((OTHER_CONTENT+1))
    record WARN "authzPolicy/${p##*/}" "$PROF on the same gateway -- precedence between two CONTENT_AUTHZ policies is undefined; another governance extension on this gateway looks like this"
  else
    record PASS "authzPolicy/${p##*/}" "$PROF -- different phase, coexists cleanly"
  fi
done <<<"$POLS"
[[ -z "$OURS" ]] && record TODO "authzPolicy" "none targets $GATEWAY yet -- created in the bind step, last of all"

# ------------------------------------------------------------------- Apigee --
if [[ -n "$ENVNAME" ]]; then
  EJ="$(api "https://apigee.googleapis.com/v1/organizations/$ORG/environments/$ENVNAME")"
  ENV_EXISTS=0
  if [[ -z "$EJ" || "$EJ" == *'"error"'* ]]; then
    record TODO "apigee/env/$ENVNAME" "not created yet -- ensure_apigee_environment.sh creates and attaches it (~4 min)"
  else
    ENV_EXISTS=1
    record PASS "apigee/env/$ENVNAME" "exists"
    # BASE rejects extensible proxies, and nothing earlier in the build says so:
    # create, attach and the property PATCH all succeed, then only the deploy
    # fails -- "Extensible proxy can not be deployed to a base environment." --
    # and it fails after the ~4 min attachment. Checked here so the read-only
    # pass can predict it.
    ETYPE="$(jqf 'd.get("type","")' <<<"$EJ")"
    if [[ "$ETYPE" == "BASE" ]]; then
      record TODO "  type" "BASE cannot host an extensible proxy -- the build PATCHes ?updateMask=type to COMPREHENSIVE before attaching"
    elif [[ -n "$ETYPE" ]]; then
      record PASS "  type" "$ETYPE"
    else
      # Healthy orgs often omit `type` entirely -- absent is NOT BASE, and
      # failing on it reports a broken setup as broken for the wrong reason.
      # The deployment check below is the real signal.
      record PASS "  type" "not reported (only an explicit BASE blocks extensible proxies)"
    fi
    SEP="$(jqf 'next((p["value"] for p in d.get("properties",{}).get("property",[]) if p.get("name")=="apigee-service-extension-enabled"),"")' <<<"$EJ")"
    if [[ "$SEP" == "true" ]]; then
      record PASS "  apigee-service-extension-enabled" "true"
    else
      record TODO "  apigee-service-extension-enabled" "${SEP:-unset} -- the build sets it; without it the proxy deploys STANDARD and never sees agent traffic"
    fi
  fi

  # An environment in more than one envgroup makes the gateway 404 every agent
  # request with the extension never invoked, and nothing anywhere reports it.
  #
  # Only meaningful once the environment exists. Running it anyway reports an
  # envgroup "in no envgroup" and then a hostname mismatch against a group that
  # was never built -- one absent resource cascading into several confident
  # failures, which is the noise this script exists to avoid.
  if (( ENV_EXISTS == 0 )); then
    record SKIP "apigee/envgroup" "not checked -- $ENVNAME does not exist yet; checked once it is created"
  else
  EGS="$(api "https://apigee.googleapis.com/v1/organizations/$ORG/envgroups")"
  INGRP="$(python3 -c '
import json,sys,urllib.request,os
d=json.loads(sys.stdin.read() or "{}")
print(" ".join(g.get("name","") for g in d.get("environmentGroups",[])))' <<<"$EGS" 2>/dev/null || true)"
  HOLDING=()
  for g in $INGRP; do
    AT="$(api "https://apigee.googleapis.com/v1/organizations/$ORG/envgroups/${g}/attachments")"
    grep -q "\"$ENVNAME\"" <<<"$AT" && HOLDING+=("$g")
  done
  case "${#HOLDING[@]}" in
    0) record TODO "apigee/envgroup" "$ENVNAME is in no envgroup yet -- the build creates one and attaches it" ;;
    1) record PASS "apigee/envgroup" "${HOLDING[0]} (exactly one, which is required)" ;;
    *) record FAIL "apigee/envgroup" "$ENVNAME is in ${#HOLDING[@]} envgroups (${HOLDING[*]}) -- the gateway 404s every request and reports nothing" ;;
  esac

  if [[ -n "$ENVGROUP" && -n "$HOSTNAME_" ]]; then
    EG="$(api "https://apigee.googleapis.com/v1/organizations/$ORG/envgroups/$ENVGROUP")"
    if [[ -z "$EG" || "$EG" == *'"error"'* ]]; then
      # The group itself is not there yet. Reporting a hostname mismatch
      # against a group that does not exist states a real problem for an
      # unreal reason, and sends the reader to check DNS.
      record TODO "  envgroup hostname" "$ENVGROUP does not exist yet -- the build creates it carrying $HOSTNAME_"
    elif grep -q "$HOSTNAME_" <<<"$EG"; then
      record PASS "  envgroup hostname" "$ENVGROUP carries $HOSTNAME_"
    else
      record FAIL "  envgroup hostname" "$ENVGROUP does not carry $HOSTNAME_ -- a hostname mismatch no build step resolves; the three names must be identical"
    fi
  fi
  fi
fi

# ------------------------------------------------------------------- VPC -----
if [[ -n "$VPC" ]]; then
  if gcloud compute networks describe "$VPC" --project="$PROJECT" >/dev/null 2>&1; then
    record PASS "vpc/$VPC" "exists  (REUSE: shared with any other extension on this gateway)"
  else
    record FAIL "vpc/$VPC" "not found"
  fi
fi
if [[ -n "$SUBNET" ]]; then
  SN="$(gcloud compute networks subnets describe "$SUBNET" --region="$REGION" \
        --project="$PROJECT" --format='value(ipCidrRange)' 2>/dev/null || true)"
  if [[ -n "$SN" ]]; then
    record PASS "subnet/$SUBNET" "$SN  (REUSE: the PSC IP is drawn from here)"
  else
    record FAIL "subnet/$SUBNET" "not found in $REGION"
  fi
fi
# The VPC and subnet are the user's own infrastructure and have no documented
# default to fall back on, so an absent flag genuinely means "not checked".
# Record that rather than omitting the row: a check that silently did not run
# is indistinguishable, in the output, from one that passed.
[[ -z "$VPC"    ]] && record SKIP "vpc"    "not checked -- pass --vpc to verify the gateway egresses into the network you expect"
[[ -z "$SUBNET" ]] && record SKIP "subnet" "not checked -- pass --subnet to verify the PSC IP is drawn from the right range"

if [[ -n "$ENVNAME" && -n "$PROXY" ]]; then
  DEP="$(api "https://apigee.googleapis.com/v1/organizations/$ORG/environments/$ENVNAME/apis/$PROXY/deployments")"
  REV="$(jqf 'd.get("deployments",[{}])[0].get("revision","")' <<<"$DEP")"
  DT="$(jqf 'd.get("deployments",[{}])[0].get("proxyDeploymentType","")' <<<"$DEP")"
  if [[ -z "$REV" ]]; then
    record TODO "apigee/proxy/$PROXY" "not deployed yet -- deploy_proxy.sh builds and deploys it (~2 min)"
  elif [[ "$DT" == "EXTENSIBLE" ]]; then
    record PASS "apigee/proxy/$PROXY" "rev $REV, EXTENSIBLE"
  else
    record FAIL "apigee/proxy/$PROXY" "rev $REV, ${DT:-unknown} -- STANDARD deploys clean and governs nothing"
  fi

  # Which features are actually DEPLOYED, read off the revision's policy list
  # rather than inferred from config. Drives the Enforcement rollup row: this
  # skill meters without blocking, EXCEPT Model Armor, which is
  # continueOnError=false and fails a turn closed.
  if [[ -n "$REV" ]]; then
    POLJ="$(api "https://apigee.googleapis.com/v1/organizations/$ORG/apis/$PROXY/revisions/$REV")"
    [[ "$POLJ" == *modelarmor* ]]     && HAS_ARMOR=1
    [[ "$POLJ" == *LTQ-count* ]]      && HAS_METER=1
    [[ "$POLJ" == *semanticcache* ]]  && HAS_CACHE=1
    [[ "$POLJ" == *LTQ-enforce* ]]    && HAS_ENFORCE=1

    # Model Armor is the only policy that can refuse a request, so read its
    # ACTUAL enforcement mode rather than trusting the config. continueOnError
    # is not exposed on any JSON endpoint -- there is no per-policy resource --
    # so pull the revision bundle. It is ~10 KB and about half a second.
    if [[ "${HAS_ARMOR:-0}" == "1" ]]; then
      BUNDLE="$(mktemp)"
      if curl -fsS -H "Authorization: Bearer $TOKEN" -o "$BUNDLE" \
           "https://apigee.googleapis.com/v1/organizations/$ORG/apis/$PROXY/revisions/$REV?format=bundle" 2>/dev/null; then
        MA_COE="$(python3 - "$BUNDLE" <<'PY' 2>/dev/null || true
import sys,zipfile,re
try:
    z=zipfile.ZipFile(sys.argv[1])
    for n in z.namelist():
        if "modelarmor" in n and n.endswith(".xml"):
            m=re.search(r'continueOnError="(\w+)"', z.read(n).decode())
            if m: print(m.group(1)); break
except Exception:
    pass
PY
)"
      fi
      rm -f "$BUNDLE"
      [[ "$MA_COE" == "true" ]] && MA_MODE="DRY_RUN" || MA_MODE="ENFORCE"
      [[ -z "$MA_COE" ]] && MA_MODE="unknown"
    fi
  fi
fi

# ------------------------------------------------------------------ the PSC --
if [[ -n "$HOSTNAME_" ]]; then
  # Matched on TARGET, not name: the one pointing at an Apigee instance
  # service attachment is ours whatever it happens to be called. Falls back to
  # the name hint for a half-built setup whose target is not resolvable yet.
  FR="$(gcloud compute forwarding-rules list --project="$PROJECT" \
        --filter="region:($REGION)" \
        --format='value(name,IPAddress,pscConnectionStatus,target)' 2>/dev/null || true)"
  PSCIP="$(awk '$4 ~ /serviceAttachments\/apigee-/ {print $2; exit}' <<<"$FR")"
  PSCST="$(awk '$4 ~ /serviceAttachments\/apigee-/ {print $3; exit}' <<<"$FR")"
  if [[ -z "$PSCIP" ]]; then
    PSCIP="$(awk -v m="$OUR_PSC_MATCH" '$0 ~ m {print $2; exit}' <<<"$FR")"
    PSCST="$(awk -v m="$OUR_PSC_MATCH" '$0 ~ m {print $3; exit}' <<<"$FR")"
  fi
  if [[ -z "$PSCIP" ]]; then
    record TODO "psc/endpoint" "none yet in $REGION -- the build CREATEs one targeting the Apigee instance service attachment (never shared with another extension)"
  elif [[ "$PSCST" == "ACCEPTED" ]]; then
    record PASS "psc/endpoint" "$PSCIP ACCEPTED"
  else
    record FAIL "psc/endpoint" "$PSCIP ${PSCST:-PENDING} -- project is probably not on the instance consumerAcceptList"
  fi

  ZN="$(gcloud dns managed-zones list --project="$PROJECT" --format='value(name,dnsName)' 2>/dev/null || true)"
  PARENT="${HOSTNAME_#*.}."
  if grep -q "$PARENT" <<<"$ZN"; then
    ZNAME="$(awk -v p="$PARENT" '$2==p {print $1; exit}' <<<"$ZN")"
    record PASS "dns/zone" "${ZNAME:-found} covers $PARENT"
    RS="$(gcloud dns record-sets list --zone="${ZNAME}" --project="$PROJECT" \
          --filter="name=${HOSTNAME_}." --format='value(rrdatas[0])' 2>/dev/null || true)"
    if [[ -z "$RS" ]]; then
      record TODO "dns/record" "no A record for $HOSTNAME_ yet -- the build CREATEs it once the PSC IP exists"
    elif [[ -n "$PSCIP" && "$RS" != "$PSCIP" ]]; then
      record FAIL "dns/record" "$HOSTNAME_ -> $RS but the PSC endpoint is $PSCIP"
    else
      record PASS "dns/record" "$HOSTNAME_ -> $RS"
    fi
  else
    record TODO "dns/zone" "no private zone covers $PARENT yet -- the build CREATEs one (an existing parent zone is reused instead)"
  fi
fi

# --------------------------------------------------------- Vector Search ----
# Only reached when the deployed revision actually carries the cache policies,
# so this never probes Vertex AI for a setup that does not use it.
#
# The deployed index is the ONE resource in this skill that bills while idle.
# The provisioning script prints a COST block and modes.md requires explicit
# confirmation before creating it -- and then the health check said nothing
# about it at all, so an operator auditing an unfamiliar project got
# "SETUP OK, nothing outstanding" while a replica had been running for hours.
# Having taken the cost seriously at create time, reporting it afterwards is
# the other half of the same obligation.
CACHE_INDEX_ID=""; CACHE_EP_ID=""; CACHE_MACHINE=""; CACHE_REPLICAS=""
CACHE_DIMS=""; CACHE_METHOD=""; CACHE_SYNC=""; CACHE_DEPLOYED=""; CACHE_ELAPSED=""
if [[ "${HAS_CACHE:-0}" == "1" ]]; then
  IDX_JSON="$(gcloud ai indexes list --project="$PROJECT" --region="$REGION" \
              --format=json 2>/dev/null || echo '[]')"
  CACHE_INDEX_ID="$(jqf 'next((i["name"].split("/")[-1] for i in d if "cache" in i.get("displayName","").lower()), "")' <<<"$IDX_JSON")"
  if [[ -n "$CACHE_INDEX_ID" ]]; then
    CACHE_DIMS="$(jqf 'next((str(i.get("metadata",{}).get("config",{}).get("dimensions","")) for i in d if i["name"].endswith("'"$CACHE_INDEX_ID"'")), "")' <<<"$IDX_JSON")"
    CACHE_METHOD="$(jqf 'next((i.get("indexUpdateMethod","") for i in d if i["name"].endswith("'"$CACHE_INDEX_ID"'")), "")' <<<"$IDX_JSON")"
    if [[ "$CACHE_METHOD" == "STREAM_UPDATE" ]]; then
      record PASS "vectorsearch/index" "$CACHE_INDEX_ID  dims=${CACHE_DIMS:-?} $CACHE_METHOD"
    else
      # Not cosmetic: SemanticCachePopulate writes via :upsertDatapoints, which
      # a BATCH_UPDATE index does not expose. Populate fails silently forever.
      record FAIL "vectorsearch/index" "$CACHE_INDEX_ID is ${CACHE_METHOD:-unknown}, not STREAM_UPDATE -- SemanticCachePopulate writes through :upsertDatapoints and can never succeed against it"
    fi
  else
    record FAIL "vectorsearch/index" "cache policies are deployed but no index found in $REGION -- lookups cannot resolve; scripts/ensure_vector_search.sh builds it"
  fi

  EP_JSON="$(gcloud ai index-endpoints list --project="$PROJECT" --region="$REGION" \
             --format=json 2>/dev/null || echo '[]')"
  CACHE_EP_ID="$(jqf 'next((e["name"].split("/")[-1] for e in d if e.get("deployedIndexes")), "")' <<<"$EP_JSON")"
  if [[ -n "$CACHE_EP_ID" ]]; then
    CACHE_MACHINE="$(jqf 'next((di.get("dedicatedResources",{}).get("machineSpec",{}).get("machineType","") for e in d for di in e.get("deployedIndexes",[])), "")' <<<"$EP_JSON")"
    CACHE_REPLICAS="$(jqf 'next((str(di.get("dedicatedResources",{}).get("minReplicaCount","")) for e in d for di in e.get("deployedIndexes",[])), "")' <<<"$EP_JSON")"
    CACHE_SYNC="$(jqf 'next((di.get("indexSyncTime","") for e in d for di in e.get("deployedIndexes",[])), "")' <<<"$EP_JSON")"
    CACHE_DEPLOYED="$(jqf 'next((di.get("createTime","") for e in d for di in e.get("deployedIndexes",[])), "")' <<<"$EP_JSON")"

    # "Bills per node-hour" is a true statement nobody acts on. The number
    # someone reviewing an idle demo environment actually wants is how long it
    # has been running, and that is derivable from the deployedIndex
    # createTime. No pricing table: the duration alone turns an abstract
    # warning into something you can decide about, and a rate would go stale.
    CACHE_ELAPSED=""
    if [[ -n "$CACHE_DEPLOYED" ]]; then
      _then="$(date -d "$CACHE_DEPLOYED" +%s 2>/dev/null || echo "")"
      if [[ -n "$_then" ]]; then
        _secs=$(( $(date +%s) - _then )); (( _secs < 0 )) && _secs=0
        CACHE_ELAPSED="  deployed $(( _secs / 3600 ))h$(( (_secs % 3600) / 60 ))m ago -- ~$(awk -v s="$_secs" -v r="${CACHE_REPLICAS:-1}" 'BEGIN{printf "%.1f", (s/3600.0)*r}') node-hours accrued"
      fi
    fi
    record WARN "vectorsearch/deployed" "${CACHE_MACHINE:-?} x${CACHE_REPLICAS:-?} -- BILLING per node-hour while deployed, with or without traffic${CACHE_ELAPSED}${CACHE_SYNC:+  (last sync $CACHE_SYNC)}; scripts/teardown_vector_search.sh stops it, in order"
  else
    record FAIL "vectorsearch/endpoint" "cache policies are deployed but no index endpoint carries a deployed index -- every lookup fails; scripts/ensure_vector_search.sh deploys one"
  fi
fi

# ------------------------------------------------------------------ rollup --
# A category rollup above the per-check table. The table answers "which check
# failed"; this answers "what is this setup, and what does it do to traffic" --
# which is the question someone arriving cold actually has, and which 20 rows
# of PASS do not answer. Status carries a VALUE, not just a verdict, and each
# Details cell states the consequence rather than restating the value.
SUMROWS=()
sumrow() { SUMROWS+=("$1|$2|$3"); }

# Overall Health is computed LAST and PREPENDED -- see `rollup_overall_health`
# just before the output section. It is the first row the reader sees, but it
# summarises counters that rollup rows below are still incrementing, so
# building it here reads them too early and under-reports.

if [[ -z "${REV:-}" ]]; then
  sumrow "Proxy" "NOT DEPLOYED" "nothing is governing traffic yet"
else
  sumrow "Proxy" "${DT:-unknown} rev ${REV}" "${PROXY:-?} on ${ENVNAME:-?}$([[ "${ETYPE:-}" == "BASE" ]] && echo "  -- env is BASE and cannot host this")"
fi

# Other governance products surface a row like this as Enforcement Mode. Ours
# is a different answer, and it should be stated rather than left to be
# inferred from a hardcoded CountOnly.
if [[ "${HAS_ARMOR:-0}" == "1" && "${MA_MODE:-}" == "DRY_RUN" ]]; then
  sumrow "Enforcement" "METER + ARMOR:DRY_RUN" "nothing blocks -- Model Armor evaluates and logs, the fault is swallowed"
elif [[ "${HAS_ARMOR:-0}" == "1" && "${MA_MODE:-}" == "ENFORCE" ]]; then
  sumrow "Enforcement" "METER + ARMOR:ENFORCE${HAS_ENFORCE:+ + QUOTA LIMIT}" "Model Armor DOES refuse a matching request (400)$([[ "${HAS_ENFORCE:-0}" == "1" ]] && echo "; token budget also enforced, one request late" || echo "; quotas count only")"
elif [[ "${HAS_ARMOR:-0}" == "1" ]]; then
  sumrow "Enforcement" "METER + ARMOR:?" "Model Armor deployed; could not read continueOnError off rev ${REV:-?}"
elif [[ "${HAS_METER:-0}" == "1" && "${HAS_ENFORCE:-0}" == "1" ]]; then
  sumrow "Enforcement" "METER + QUOTA LIMIT" "token budget IS enforced: an over-budget caller is refused on its NEXT request (enforcement is one request late)"
elif [[ "${HAS_METER:-0}" == "1" ]]; then
  sumrow "Enforcement" "METER ONLY" "quotas are CountOnly -- no request is ever blocked by this proxy"
else
  sumrow "Enforcement" "NONE DETECTED" "no metering policies on rev ${REV:-?}"
fi

# The only continuously-billing component gets its own row. Absent is a real
# answer here, not a gap -- "OFF" tells an auditor there is no standing spend.
if [[ "${HAS_CACHE:-0}" == "1" ]]; then
  CACHECOST="${CACHE_MACHINE:-?} x${CACHE_REPLICAS:-?}"
  sumrow "Caching" "ON  ($CACHECOST)" "deployed index ${CACHE_INDEX_ID:-?} -- BILLING per node-hour while deployed, traffic or not"
else
  sumrow "Caching" "OFF" "no semantic cache policies on rev ${REV:-?}; nothing here bills while idle"
fi

if [[ -n "${OUR_SUF:-}" ]]; then
  NSUF="$(awk -F, '{print NF}' <<<"$OUR_SUF")"
  CACHENOTE=""
  if [[ "${HAS_CACHE:-0}" == "1" && "${NSUF:-1}" -gt 1 ]]; then
    CACHENOTE="  -- KNOWN ISSUE: cache + >1 shape can serve the wrong model's answer"
    # Also a row in its own right. modes.md requires this warning "at plan
    # time and again in the summary", and assess is where someone inspecting
    # a setup they did not build will look for it.
    record WARN "semanticcache/shapes" "cache is ON with $NSUF governed shapes -- the cache key is the prompt embedding alone, carrying no model or wire-shape discriminator, so a cross-shape hit returns an EMPTY HTTP 200 that reads as the agent being broken. Treat hits as unverified while more than one model sits behind this proxy"
  fi
  sumrow "Governed Shapes" "$NSUF" "${OUR_SUF}${CACHENOTE}"
else
  sumrow "Governed Shapes" "0" "no AuthzPolicy suffixes -- nothing reaches Apigee"
fi

if [[ "${PSCST:-}" == "ACCEPTED" && -n "${ZNAME:-}" ]]; then
  sumrow "Callout Path" "Verified" "PSC ${PSCIP:-?} ACCEPTED, zone ${ZNAME} resolves ${HOSTNAME_:-?}"
else
  sumrow "Callout Path" "Incomplete" "PSC=${PSCST:-missing}, dns zone=${ZNAME:-missing} -- the callout cannot land"
fi

if [[ -n "${OURS:-}" ]]; then
  sumrow "AuthZ Wiring" "Verified" "${OURS}$( (( ${OTHER_CONTENT:-0} > 0 )) && echo "  -- plus ${OTHER_CONTENT} other CONTENT_AUTHZ policy; precedence undefined")"
else
  sumrow "AuthZ Wiring" "Missing" "no policy targets ${GATEWAY:-?}"
fi

# ------------------------------------------------- overall health (last) ----
# Deliberately the last thing computed and the first thing shown.
#
# Overall health reads TODO and FAIL as different kinds of news. A greenfield
# project is not a broken one: all TODO and no FAIL means there is nothing to
# repair, only things to build, and the headline has to say so or the whole
# run reads as breakage.
#
# It must read the SAME accumulators the footer tally prints. Computing it
# earlier -- where it used to live, above the rollup rows -- took a snapshot
# before `semanticcache/shapes` recorded its WARN, so a run with two warnings
# announced one. The dropped one was either the billing disclosure or the
# cache-correctness known issue, and modes.md tells the agent to lead with
# this row and treat it as the answer.
TALLY="$PASS PASS, $FAILN FAIL, $WARN WARN, $TODO TODO"
if   (( FAILN > 0 && TODO > 0 )); then
  OVERALL="NEEDS WORK"
  DETAIL="$TALLY -- fix the $FAILN failure(s); the $TODO outstanding build steps are not faults"
elif (( FAILN > 0 )); then
  OVERALL="NEEDS WORK"
  DETAIL="$TALLY -- $FAILN genuine failure(s) to fix"
elif (( TODO > 0 && PASS <= 2 )); then
  OVERALL="NOT BUILT"
  DETAIL="$TALLY -- nothing built yet and nothing broken; a clean starting point"
elif (( TODO > 0 )); then
  OVERALL="PARTIALLY BUILT"
  DETAIL="$TALLY -- no failures; $TODO step(s) left to finish the build"
elif (( WARN > 0 )); then
  OVERALL="OK, WITH NOTES"
  DETAIL="$TALLY -- built and healthy; warnings are things to know, not to fix"
else
  OVERALL="SETUP OK"
  DETAIL="$TALLY -- built and healthy"
fi
SUMROWS=("Overall Health|$OVERALL|$DETAIL" "${SUMROWS[@]}")

# ------------------------------------------------------------------- output --
if (( JSON )); then
  python3 -c '
import json,sys
blocks=sys.stdin.read().split("\x02")
summ=[l.split("|",2) for l in blocks[0].splitlines() if l]
rows=[l.split("|",2) for l in blocks[1].splitlines() if l]
print(json.dumps({
  "summary":{"pass":int(sys.argv[1]),"fail":int(sys.argv[2]),"warn":int(sys.argv[3]),
             "todo":int(sys.argv[4]),"overall":sys.argv[5],
             "skip":int(sys.argv[6]),"assumed":[a for a in sys.argv[7].split() if a]},
  "rollup":[{"category":c,"status":s,"detail":d} for c,s,d in summ],
  "checks":[{"status":s,"resource":r,"detail":d} for s,r,d in rows]}, indent=2))
' "$PASS" "$FAILN" "$WARN" "$TODO" "$OVERALL" "$SKIPN" "${ASSUMED[*]:-}" <<<"$(printf '%s\n' "${SUMROWS[@]}")$(printf '\x02')$(printf '%s\n' "${ROWS[@]}")"
else
  # Box-drawn so the two tables read as tables rather than as loose columns,
  # and so the summary is visibly the headline rather than a preamble.
  rule() { printf '%s%s%s\n' "$C_DIM" "$(printf '─%.0s' $(seq 1 "$1"))" "$C_RST"; }

  case "$OVERALL" in
    "SETUP OK"|"OK, WITH NOTES") OC="$C_GRN" ;;
    "NEEDS WORK")                OC="$C_RED" ;;
    *)                           OC="$C_BLU" ;;
  esac

  hdr "Setup Status Summary"
  printf '%s %-17s %-24s %s%s\n' "$C_BLD" "CATEGORY" "STATUS" "DETAILS" "$C_RST"
  for r in "${SUMROWS[@]}"; do
    cat_="${r%%|*}"; st="$(cut -d'|' -f2 <<<"$r")"; det="${r#*|*|}"
    if [[ "$cat_" == "Overall Health" ]]; then
      printf ' %-17s %s%-24s%s %s\n' "$cat_" "$OC$C_BLD" "$st" "$C_RST" "$det"
    else
      printf ' %-17s %-24s %s\n' "$cat_" "$st" "$det"
    fi
  done
  rule 96

  hdr "Checks"
  printf '%s %-6s %-34s %s%s\n' "$C_BLD" "STATUS" "RESOURCE" "DETAIL" "$C_RST"
  for r in "${ROWS[@]}"; do
    printf ' %s %-34s %s\n' "$(paint "${r%%|*}")" "$(cut -d'|' -f2 <<<"$r")" "${r#*|*|}"
  done
  rule 96

  printf '\n %s%d PASS%s   %s%d FAIL%s   %s%d WARN%s   %s%d TODO%s   %s%d SKIP%s\n' \
    "$C_GRN" "$PASS" "$C_RST" "$C_RED" "$FAILN" "$C_RST" \
    "$C_YEL" "$WARN" "$C_RST" "$C_BLU" "$TODO" "$C_RST" \
    "$C_DIM" "$SKIPN" "$C_RST"

  if (( ${#ASSUMED[@]} > 0 )); then
    printf ' %sAssumed documented defaults for: %s%s\n' "$C_DIM" "${ASSUMED[*]}" "$C_RST"
    printf ' %sPass the matching flags if this setup uses different names.%s\n' "$C_DIM" "$C_RST"
  fi

  # Every count above is useless on its own -- say what to do about it.
  (( TODO > 0 ))  && printf ' %sTODO%s is not a failure: the resource does not exist yet and this skill creates it.\n' "$C_BLU" "$C_RST"
  (( FAILN > 0 )) && printf ' %sFAIL%s is something a build step will NOT resolve. Fix top-down: a gateway with no\n      route into the VPC makes every later check meaningless.\n' "$C_RED" "$C_RST"
  (( FAILN == 0 && WARN > 0 )) && printf ' %sWARN%s is a thing to know, not a thing to fix.\n' "$C_YEL" "$C_RST"
  # Standing spend gets its own line. Folding it into "warnings are things to
  # know, not to fix" is wrong: this one IS actionable, and it is the only
  # thing in the skill that costs money while nothing is happening.
  [[ "${HAS_CACHE:-0}" == "1" && -n "${CACHE_MACHINE:-}" ]] && printf \
    ' %sCOST%s  the deployed index (%s x%s) bills per node-hour whether or not traffic flows.\n       Undeploy it to stop the charge -- editing the YAML does not.\n' \
    "$C_YEL" "$C_RST" "${CACHE_MACHINE}" "${CACHE_REPLICAS:-?}"
  (( FAILN == 0 && TODO == 0 && WARN == 0 )) && printf ' Nothing outstanding.\n'
fi

# TODO alone is a clean exit: a greenfield project is a valid state, and
# callers gate "is anything broken" on this. Only real failures exit non-zero.
(( FAILN > 0 )) && exit 1
exit 0
