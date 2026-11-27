#!/bin/bash
# Give an Agent Gateway a route into your VPC: a PSC-interface network
# attachment plus DNS peering for the callout domain.
#
# Without both, the gateway cannot reach a private Apigee endpoint and cannot
# resolve the callout hostname. Nothing reports this. The gateway keeps serving
# ordinary agent traffic to public Google endpoints -- that path never enters
# your VPC -- so every other check passes and only the Apigee callout fails.
#
# Three things make this worth a script rather than three commands:
#
#   1. `agent-gateways import` is a WHOLE-RESOURCE upsert. Importing a YAML
#      that carries only name + networkConfig silently drops `registries` and
#      `protocols`. This does read-modify-write off the live export so nothing
#      is lost.
#   2. `dnsPeeringConfig.targetNetwork` must be the full
#      projects/{p}/global/networks/{n}. A bare network name is rejected.
#   3. A gateway created before `protocols` was enforced exports YAML that its
#      own import rejects -- the API marks the field "Optional. Deprecated."
#      while gcloud requires it client-side. PROTOCOL_UNSPECIFIED is injected
#      when the export lacks it.
#
# It modifies a resource you own, so it applies nothing without --yes.
#
# Data goes to stdout as JSON. Diagnostics go to stderr.

set -euo pipefail

usage() {
  cat <<'EOF'
Ensure an Agent Gateway can reach your VPC.

Usage:
  ensure_gateway_connectivity.sh --gateway GW --project P --region R \
      --vpc VPC --subnet SUBNET --attachment NAME --domain DOMAIN [options]

Required:
  --gateway GW       Agent Gateway short name
  --project P        project holding the gateway, VPC and attachment
  --region R         must match the gateway and the Apigee instance
  --vpc VPC          VPC the gateway will egress into
  --subnet SUBNET    subnet in --region for the network attachment
  --attachment NAME  network attachment; created if absent, reused if present
  --domain DOMAIN    private DNS domain to peer, trailing dot
                     (e.g. internal.example.local.)

Options:
  --zone NAME        private DNS zone to create for --domain when none exists.
                     The import is rejected outright if the domain has no
                     private zone in --vpc. Default: agent-gw-zone

  --yes              apply. Without it, prints the diff and exits 0.
  --help             this text

Environment:
  CLOUDSDK_AUTH_ACCESS_TOKEN   set from ADC if unset.

Exit codes:
  0  already correct, or diff shown, or applied
  1  usage error
  2  precondition failed (missing subnet, gateway not found)
  3  import failed or gateway still lacks networkConfig afterwards
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

GATEWAY=""; PROJECT=""; REGION=""; VPC=""; SUBNET=""; ATTACHMENT=""; DOMAIN=""; APPLY=0; ZONE="agent-gateway-callout-zone"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --gateway) GATEWAY="$2"; shift 2 ;;
    --project) PROJECT="$2"; shift 2 ;;
    --region) REGION="$2"; shift 2 ;;
    --vpc) VPC="$2"; shift 2 ;;
    --subnet) SUBNET="$2"; shift 2 ;;
    --attachment) ATTACHMENT="$2"; shift 2 ;;
    --domain) DOMAIN="$2"; shift 2 ;;
    --zone) ZONE="$2"; shift 2 ;;
    --yes) APPLY=1; shift ;;
    --help) usage; exit 0 ;;
    *) usage >&2; die "unknown argument: $1" 1 ;;
  esac
done

for v in GATEWAY PROJECT REGION VPC SUBNET ATTACHMENT DOMAIN; do
  [[ -n "${!v}" ]] || { usage >&2; die "missing --${v,,}" 1; }
done
[[ "$DOMAIN" == *. ]] || die "--domain must end with a dot: $DOMAIN" 1

export CLOUDSDK_AUTH_ACCESS_TOKEN="${CLOUDSDK_AUTH_ACCESS_TOKEN:-$(gcloud auth application-default print-access-token)}"

WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT

# ---------------------------------------------------------------- inspect ----
log "==> reading gateway $GATEWAY"
gcloud network-services agent-gateways export "$GATEWAY" \
  --location="$REGION" --project="$PROJECT" --destination="$WORK/before.yaml" \
  >/dev/null 2>"$WORK/export.err" \
  || { cat "$WORK/export.err" >&2; die "cannot export gateway $GATEWAY" 2; }

# Surfacing an existing CUSTOM AuthzPolicy is informational. What is established:
# it cannot be merged with a new one -- `resources` is "Limited to 1 custom
# provider" and `policyProfile` is immutable -- so a second policy has to sit
# alongside it, or replace it.
#
# Deleting it is NOT known to break the gateway. On a live gateway the IAP
# CUSTOM policy was deleted during root-cause isolation, was not auto-recreated,
# and the gateway kept serving agent traffic with only the ext-proc policy
# attached. Whether it is safe in a given project depends on what relies on that
# policy, which this script cannot know -- so it reports and does not advise.
#
# Two CUSTOM policies coexisting is also NOT the cause of the 404-with-no-error
# failure; that is the environment's envgroup count. See references/gotchas.md,
# which lists a second CUSTOM policy as an individually disproved non-cause.
EXISTING_AUTHZ="$(gcloud network-security authz-policies list \
  --location="$REGION" --project="$PROJECT" --format='value(name)' 2>/dev/null \
  | while read -r pol; do
      [[ -z "$pol" ]] && continue
      if gcloud network-security authz-policies describe "${pol##*/}" \
           --location="$REGION" --project="$PROJECT" --format='value(action,target.resources)' 2>/dev/null \
         | grep -q "CUSTOM.*$GATEWAY"; then printf '%s ' "${pol##*/}"; fi
    done)"
if [[ -n "$EXISTING_AUTHZ" ]]; then
  log "NOTE: gateway $GATEWAY already has a CUSTOM AuthzPolicy: $EXISTING_AUTHZ"
  log "      It cannot be merged with a new one (one custom provider per policy,"
  log "      immutable policyProfile), so the ext-proc policy will sit alongside it."
  log "      Removing it may be safe -- check what depends on it first."
fi

# The two legs are INDEPENDENT and are detected separately. Testing for the
# `networkConfig:` block instead is the bug this comment exists to prevent: a
# gateway with egress attached but no DNS peering -- the exact state
# assess_integration.sh flags as
#   dnsPeeringConfig  absent -- ensure_gateway_connectivity.sh appends the domain
# -- took the early exit and reported "nothing to do". assess named this
# script as the remedy, this script declined to act, both exited 0, and the
# callout could not resolve its hostname while every later step passed.
HAS_EGRESS=0
grep -q 'networkAttachment:' "$WORK/before.yaml" && HAS_EGRESS=1
HAS_PEERING=0
grep -q 'dnsPeeringConfig:' "$WORK/before.yaml" && HAS_PEERING=1

# Whether the block exists is NOT the same question as whether OUR domain is in
# it. A gateway can already peer a different extension's domain -- the block is
# present, `domains` does not contain $DOMAIN, and the correct action is to
# APPEND to the list rather than to do nothing. Treating "block present" as
# "done" is the same class of bug as the one the comment above describes: the
# callout cannot resolve its hostname while every later step still passes.
DOMAIN_LISTED=0
if [[ $HAS_PEERING -eq 1 ]]; then
  PRE_DOMAINS="$(gcloud network-services agent-gateways describe "$GATEWAY" \
    --location="$REGION" --project="$PROJECT" \
    --format='value(networkConfig.dnsPeeringConfig.domains)' 2>/dev/null || true)"
  # gcloud joins a repeated field with ';'. Wrap both sides so the match is
  # exact and a domain cannot match a longer one that merely contains it.
  case ";$(printf '%s' "$PRE_DOMAINS" | tr -d '[:space:]');" in
    *";$DOMAIN;"*) DOMAIN_LISTED=1 ;;
  esac
fi

if [[ $HAS_EGRESS -eq 1 && $DOMAIN_LISTED -eq 1 ]]; then
  log "    egress attachment and DNS peering for $DOMAIN both present -- nothing to do"
  printf '{"changed":false,"reason":"egress and dnsPeeringConfig both present","gateway":"%s"}\n' "$GATEWAY"
  exit 0
fi

if [[ $HAS_EGRESS -eq 1 && $HAS_PEERING -eq 1 ]]; then
  log "    egress present, dnsPeeringConfig present but WITHOUT $DOMAIN -- appending"
elif [[ $HAS_EGRESS -eq 1 ]]; then
  log "    egress present, dnsPeeringConfig ABSENT -- gateway cannot resolve $DOMAIN"
elif [[ $HAS_PEERING -eq 1 ]]; then
  log "    dnsPeeringConfig present, egress ABSENT -- gateway has no route into $VPC"
else
  log "    networkConfig ABSENT -- gateway has no route into $VPC"
fi

gcloud compute networks subnets describe "$SUBNET" \
  --region="$REGION" --project="$PROJECT" >/dev/null 2>&1 \
  || die "subnet $SUBNET not found in $REGION" 2

# The import validates dnsPeeringConfig.domains against EXISTING private zones in
# the target VPC and rejects the whole request if the domain has no zone:
#   domain "x." does not exist as a private zone in network ".../networks/<vpc>"
# The zone may be empty -- only its existence is checked. The A record cannot be
# written yet anyway, since the PSC endpoint it points at comes later.
ZONE_EXISTS=0
EXISTING_ZONE="$(gcloud dns managed-zones list --project="$PROJECT" \
  --filter="dnsName=$DOMAIN AND visibility=private" --format='value(name)' 2>/dev/null | head -1)"
if [[ -n "$EXISTING_ZONE" ]]; then
  ZONE_EXISTS=1
  ZONE="$EXISTING_ZONE"
fi

ATTACH_URI="projects/$PROJECT/regions/$REGION/networkAttachments/$ATTACHMENT"
ATTACH_EXISTS=0
gcloud compute network-attachments describe "$ATTACHMENT" \
  --region="$REGION" --project="$PROJECT" >/dev/null 2>&1 && ATTACH_EXISTS=1

# ------------------------------------------------------------ build after ----
# Read-modify-write: start from the live export so registries, protocols and
# googleManaged survive. Append rather than regenerate.
cp "$WORK/before.yaml" "$WORK/after.yaml"

# Trap 3: a gateway predating client-side enforcement exports without
# `protocols`, and its own import then rejects it.
if ! grep -q '^protocols:' "$WORK/after.yaml"; then
  log "    export lacks 'protocols' -- injecting PROTOCOL_UNSPECIFIED so import is accepted"
  printf 'protocols:\n- PROTOCOL_UNSPECIFIED\n' >>"$WORK/after.yaml"
fi

# Greenfield appends the whole block. When one leg already exists the block is
# there too, so the missing leg is INSERTED UNDER IT -- appending a second
# top-level `networkConfig:` would either be rejected or silently clobber the
# leg already in place, which for egress is the irreversible one.
#
# awk, not sed: the inserted text is multi-line and contains slashes, and the
# insert must happen exactly once even though `networkConfig:` appears in the
# comment-free export only at column 0.
_insert_under_networkconfig() {
  awk -v block="$1" '
    !done && /^networkConfig:[[:space:]]*$/ { print; printf "%s", block; done=1; next }
    { print }
    END { if (!done) exit 9 }
  ' "$WORK/after.yaml" >"$WORK/after.yaml.tmp" \
    || die "export has no top-level 'networkConfig:' to insert under -- refusing to guess" 3
  mv "$WORK/after.yaml.tmp" "$WORK/after.yaml"
}

# Adds one entry to an EXISTING dnsPeeringConfig.domains list, at the same
# indentation as the `domains:` key -- the shape PEERING_BLOCK below writes and
# the shape gcloud exports. Additive only: the entries already there are left
# untouched, because another extension depends on them.
_append_domain_to_peering() {
  awk -v dom="$DOMAIN" '
    /^[[:space:]]*domains:[[:space:]]*$/ && !done {
      print
      match($0, /^[[:space:]]*/)
      print substr($0, 1, RLENGTH) "- " dom
      done = 1
      next
    }
    { print }
    END { if (!done) exit 9 }
  ' "$WORK/after.yaml" >"$WORK/after.yaml.tmp" \
    || die "dnsPeeringConfig present but has no 'domains:' list to append to -- refusing to guess" 3
  mv "$WORK/after.yaml.tmp" "$WORK/after.yaml"
}

PEERING_BLOCK="  dnsPeeringConfig:
    domains:
    - $DOMAIN
    targetNetwork: projects/$PROJECT/global/networks/$VPC
    targetProject: $PROJECT
"
EGRESS_BLOCK="  egress:
    networkAttachment: $ATTACH_URI
"

if [[ $HAS_EGRESS -eq 0 && $HAS_PEERING -eq 0 ]]; then
  # printf, not a heredoc: both blocks already carry their trailing newline,
  # and a heredoc terminator has to sit alone at the start of a source line.
  printf 'networkConfig:\n%s%s' "$EGRESS_BLOCK" "$PEERING_BLOCK" >>"$WORK/after.yaml"
elif [[ $HAS_PEERING -eq 0 ]]; then
  log "    inserting dnsPeeringConfig into the existing networkConfig"
  _insert_under_networkconfig "$PEERING_BLOCK"
else
  # Peering block exists. Append our domain if it is missing -- never replace
  # the list, which would unpeer whoever is already using this gateway.
  if [[ $DOMAIN_LISTED -eq 0 ]]; then
    log "    appending $DOMAIN to the existing dnsPeeringConfig.domains"
    _append_domain_to_peering
  fi
  if [[ $HAS_EGRESS -eq 0 ]]; then
    log "    inserting egress attachment into the existing networkConfig"
    _insert_under_networkconfig "$EGRESS_BLOCK"
  fi
fi

# --------------------------------------------------- egress reachability ----
# Attaching egress PINS ALL the gateway's egress into this VPC -- not just the
# Apigee callout. The agents' own control-plane calls (create_session, and the
# model call itself) start leaving through here too. If this VPC cannot reach
# Google APIs, every agent behind the gateway stops working.
#
# Checked BEFORE the diff, because the diff cannot show it: the change is
# purely additive on paper -- a networkConfig block appears, nothing is
# removed -- so it reads as safe while being a routing change. And it is NOT
# reversible (see the warning below), so a wrong answer here is expensive.
#
# ONLY when egress is actually being attached. If the gateway is already
# pinned and all we are adding is DNS peering, the pinning decision was taken
# long ago and this check can no longer protect anything -- it would just
# refuse the peering fix on a gateway whose callout is already broken, which
# is the worst moment to withhold the remedy.
SUBNET_PGA="n/a"
NAT_COUNT=0
if [[ $HAS_EGRESS -eq 0 ]]; then
SUBNET_PGA="$(gcloud compute networks subnets describe "$SUBNET" \
  --region="$REGION" --project="$PROJECT" \
  --format='value(privateIpGoogleAccess)' 2>/dev/null || echo "")"
NAT_COUNT="$(gcloud compute routers list --project="$PROJECT" \
  --filter="region:($REGION) AND network:($VPC)" \
  --format='value(name)' 2>/dev/null | grep -c . || true)"

if [[ "$SUBNET_PGA" != "True" && "${NAT_COUNT:-0}" -eq 0 ]]; then
  log ""
  log "!! REFUSING: subnet '$SUBNET' has privateIpGoogleAccess=${SUBNET_PGA:-unset} and"
  log "!! there is no Cloud NAT on network '$VPC' in $REGION."
  log "!!"
  log "!! Pinning gateway egress into a VPC that cannot reach *.googleapis.com"
  log "!! takes EVERY agent behind this gateway offline, not just the Apigee"
  log "!! callout -- the agents' own create_session calls egress here too. The"
  log "!! symptom is an agent-side connection reset to"
  log "!! <region>-aiplatform.mtls.googleapis.com, which reads as an agent bug."
  log "!!"
  log "!! Fix one of these first, then re-run:"
  log "!!   gcloud compute networks subnets update $SUBNET --region=$REGION \\"
  log "!!     --project=$PROJECT --enable-private-ip-google-access"
  log "!!   (or create a Cloud NAT on $VPC in $REGION)"
  die "VPC egress cannot reach Google APIs; refusing to pin gateway egress into it" 2
fi
log "    egress reachability: privateIpGoogleAccess=$SUBNET_PGA, CloudNAT routers=$NAT_COUNT -- OK"
else
  log "    egress already attached -- reachability check skipped, pinning is not being changed"
fi

# ------------------------------------------------------------------ diff -----
# The one-way warning belongs to the EGRESS leg only. Printing it when all we
# are adding is DNS peering trains the reader to scroll past the loudest
# warning in the skill, which is how it stops working the day it matters.
log ""
if [[ $HAS_EGRESS -eq 0 ]]; then
  log "!! ONE-WAY CHANGE. egress.networkAttachment is settable once and IMMUTABLE"
  log "!! afterwards -- removing it is itself a mutation and is rejected:"
  log "!!   \"network attachment is not mutable\""
  log "!! The attachment cannot be deleted while the gateway holds it either"
  log "!! (\"Network Attachment with connected endpoints cannot be deleted\")."
  log "!! The only way back is deleting and recreating the Agent Gateway, which"
  log "!! means rebinding every agent -- and agent_gateway_config is set at agent"
  log "!! CREATION time, so in practice the agents get redeployed."
  log "!! This is the only script here that changes a resource you already own"
  log "!! in a way you cannot undo."
  log ""
fi
hdr "Proposed change to $GATEWAY"
if [[ $ZONE_EXISTS -eq 1 ]]; then
  row REUSE "private DNS zone $ZONE for $DOMAIN"
else
  row CREATE "private DNS zone $ZONE for $DOMAIN -- the import is rejected without it"
fi
if [[ $HAS_EGRESS -eq 1 ]]; then
  row REUSE "network attachment (gateway egress already attached)"
elif [[ $ATTACH_EXISTS -eq 1 ]]; then
  row REUSE "network attachment $ATTACHMENT"
else
  row CREATE "network attachment $ATTACHMENT"
fi
if [[ $HAS_EGRESS -eq 1 ]]; then
  row MODIFY "$GATEWAY -- DNS peering for $DOMAIN only (diff below)"
elif [[ $HAS_PEERING -eq 1 ]]; then
  row MODIFY "$GATEWAY -- egress attachment only (diff below)"
else
  row MODIFY "$GATEWAY -- egress attachment and DNS peering (diff below)"
fi
log ""
diff -u "$WORK/before.yaml" "$WORK/after.yaml" >&2 || true
log ""
# The single most consequential warning in the skill, and it used to be in
# prose elsewhere rather than at the point of consent. Gated with the leg it
# describes -- see the note above the diff.
if [[ $HAS_EGRESS -eq 0 ]]; then
  cost "IRREVERSIBLE  egress.networkAttachment is immutable once set, and it pins"
  cost "              ALL of this gateway's egress into that VPC -- not just the"
  cost "              Apigee callout. Agents already running can lose access to"
  cost "              Google APIs unless the subnet has Private Google Access or"
  cost "              a Cloud NAT. Capture a known-good agent turn before applying."
  log ""
fi

if [[ $APPLY -ne 1 ]]; then
  printf '  %sNot applying.%s Re-run with %s--yes%s to make these changes.\n' \
    "$C_BLD" "$C_RST" "$C_BLD" "$C_RST" >&2
  printf '{"changed":false,"reason":"dry run, --yes not given","gateway":"%s","attachmentExists":%s}\n' \
    "$GATEWAY" "$([[ $ATTACH_EXISTS -eq 1 ]] && echo true || echo false)"
  exit 0
fi

# ----------------------------------------------------------------- apply -----
if [[ $ZONE_EXISTS -eq 0 ]]; then
  log "==> creating private DNS zone $ZONE for $DOMAIN"
  gcloud dns managed-zones create "$ZONE" \
    --dns-name="$DOMAIN" --visibility=private \
    --networks="$VPC" --description="Agent Gateway ext-proc callout zone" \
    --project="$PROJECT" >/dev/null
fi

if [[ $ATTACH_EXISTS -eq 0 ]]; then
  log "==> creating network attachment $ATTACHMENT"
  gcloud compute network-attachments create "$ATTACHMENT" \
    --region="$REGION" --subnets="$SUBNET" \
    --connection-preference=ACCEPT_AUTOMATIC \
    --project="$PROJECT" >/dev/null
fi

# The export carries an etag, so a concurrent edit fails the import instead of
# being silently overwritten.
log "==> importing gateway with networkConfig"
gcloud network-services agent-gateways import "$GATEWAY" \
  --source="$WORK/after.yaml" --location="$REGION" --project="$PROJECT" \
  >/dev/null 2>"$WORK/import.err" \
  || { cat "$WORK/import.err" >&2; die "import failed -- gateway unchanged" 3; }

# Verify the leg that was actually added, not just that networkConfig exists.
# Checking only egress passes trivially in the peering-only case -- egress was
# already there before the import -- so a peering insert that silently did
# nothing would still be reported as success. That is the same shape of
# false-green this script was just fixed for.
log "==> verifying"
ACTUAL="$(gcloud network-services agent-gateways describe "$GATEWAY" \
  --location="$REGION" --project="$PROJECT" \
  --format='value(networkConfig.egress.networkAttachment)' 2>/dev/null || true)"
[[ -n "$ACTUAL" ]] || die "import reported success but egress attachment is still absent" 3
log "    egress attachment: $ACTUAL"

PEER_DOMAINS="$(gcloud network-services agent-gateways describe "$GATEWAY" \
  --location="$REGION" --project="$PROJECT" \
  --format='value(networkConfig.dnsPeeringConfig.domains)' 2>/dev/null || true)"
case "$PEER_DOMAINS" in
  *"$DOMAIN"*) log "    dns peering:       $PEER_DOMAINS" ;;
  *) die "import reported success but dnsPeeringConfig does not list $DOMAIN (got: ${PEER_DOMAINS:-none})" 3 ;;
esac

printf '{"changed":true,"gateway":"%s","networkAttachment":"%s","dnsDomain":"%s","dnsPeeringDomains":"%s"}\n' \
  "$GATEWAY" "$ACTUAL" "$DOMAIN" "$PEER_DOMAINS"
