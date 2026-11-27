# Modes, capabilities and assessment

## Contents

-   [When the user asks what you can do](#when-the-user-asks-what-you-can-do): lines 18-113
-   [Output formatting](#output-formatting): lines 114-144
-   [Assessing an existing setup](#assessing-an-existing-setup): lines 145-276
-   [Choosing the mode](#choosing-the-mode): lines 277-296
-   [What you ask for](#what-you-ask-for): lines 297-308
-   [Defaults](#defaults): lines 309-371
-   [Start with two features, not four](#start-with-two-features-not-four): lines 372-434
-   [Discover before you plan](#discover-before-you-plan): lines 435-465
-   [The plan](#the-plan): lines 466-608
-   [What dev mode produces](#what-dev-mode-produces): lines 609-762
-   [Hard refusal](#hard-refusal): lines 763-780
-   [Reconcile, don't re-create](#reconcile-dont-re-create): lines 781-856

## When the user asks what you can do

Asked an open question — "what do you know how to do with Apigee and Agent
Gateway", "what can this skill do" — answer with the five areas below, not with
a list of files. Keep it to what is actually built; naming something that does
not exist is how a demo gets stopped.

> **1. Set it up** — wire Apigee in as an authz service extension on an Agent
> Gateway, from a conversation or from a version-controlled YAML file. Creates
> the Apigee environment, envgroup, proxy and deployment, plus the PSC endpoint,
> private DNS and the gateway binding.
>
> **2. Govern LLM traffic** — four capabilities, each a few lines of config:
> caller identity from the gateway's signed assertion, per-model token metering,
> Model Armor on prompts, and a semantic cache that answers repeats without
> calling the model.
>
> **3. Assess what is running** — a read-only health check across the whole
> setup, gateway to proxy, reporting PASS/FAIL/WARN per resource. Safe to run
> against production.
>
> **4. Explain what it found** — read a debug session against live agent traffic
> and say which agent called, which model, how many tokens, and whether anything
> was blocked.
>
> **5. Tell you what is wrong** — 63 documented failure modes, indexed by
> symptom rather than cause, because the symptom is what you have.

Then say what must already exist, as a short table and nothing more:

> | Prerequisite | What it means |
> | --- | --- |
> | **Agent Gateway** | already created; this skill never creates one |
> | **Agent on Agent Runtime** | the agent's traffic must actually route through that gateway. On Agent Runtime that is set with `agent_gateway_config` when the agent is created, and cannot be added afterwards |
> | **Apigee** | an org with a runtime instance **in the same region as the gateway**. It does not have to be the same project — the callout reaches it over PSC — but the region must match |

Then ask which of the five they want. Do not start provisioning off an open
question.

**In this opening overview only, defer these four caveats.** The scope of this
rule is the capability list above and nothing else. It is a narrow deferral of
four named items from one specific answer — it is **not** a general instruction
to be sparing with caveats, and it does not apply to any other reply. Each of
the four is true, matters, and belongs at the moment it bites:

| Caveat | Defer it to |
| --- | --- |
| enforcement is one request late, and buckets on the requested model | they ask for a hard cap, or enable `tokenMetering.mode: ENFORCE` |
| the semantic cache is unreliable across more than one wire shape | they enable the cache **and** `matchPaths` has more than one entry |
| Model Armor fails closed | they enable Model Armor |
| attaching gateway egress is irreversible | the plan reaches that step |

Volunteering these four up front trades a clear answer for a hedged one, and
the user cannot act on a caveat about a feature they have not chosen yet.

**Everywhere else, the caveat is the answer.** Once the user asks about a
specific step, resource or failure, the condition that makes it go wrong is the
substance of the reply, not an optional embellishment. Omitting it is a wrong
answer, not a concise one. Always state the gating condition when it applies:

| Answering about | Always state |
| --- | --- |
| building or deploying the proxy | the deployment must report `EXTENSIBLE`; `STANDARD` will not govern |
| the PSC endpoint or callout path | confirm `pscConnectionStatus=ACCEPTED`; the AuthzExtension is inert until the host resolves and the proxy is deployed |
| creating or attaching the environment | instance attachment **locks the environment** and takes ~4 minutes |
| Model Armor mode | `DRY_RUN` evaluates and logs but does **not** block — it is not the same as disabling Model Armor |
| a symptom with more than one precondition | every condition required, not just the first — a 401 on session create needs the gateway attached **and** a recent build |

This list is not exhaustive. The test is whether the user could act on the
answer and still be surprised; if so, the caveat was load-bearing and belonged
in the reply.

When a hard cap *is* asked for: this meters by default and **can** enforce.
`tokenMetering.mode: ENFORCE` adds a request-flow quota that refuses an
over-budget caller with a 429 before the model is called — one request late by
construction, because the turn that crosses the limit has to finish before its
cost is known. Model Armor is the other policy that refuses.

**Do not raise agent-to-tool governance or model routing unprompted.** Not in
the capability list, not as a caveat, and never as something planned. This
skill governs the agent's **LLM** traffic; those are different jobs, not
pending ones. Describing them at all — even to say they are absent — invites a
commitment nobody has made.

If the user asks directly — a per-tool quota, governing calls to an MCP
server, choosing which model a request reaches — answer once, plainly, in
terms of what this skill *does*: caller identity, per-model token metering,
Model Armor on prompts, and the semantic cache. Then move on. Do not
speculate about whether it might arrive later; you do not know, and guessing
reads as a roadmap.

Fronting an MCP server is a different **shape** regardless, which is the
durable reason rather than a scheduling one: that is a proxy with a
**target**, receiving a request and routing it onward, where this one only
inspects and returns a verdict.

## Output formatting

Every surface a human reads uses the same palette, so the skill looks like one
tool rather than five scripts and a narrator.

| Colour | Means | Where |
| --- | --- | --- |
| green | exists, untouched, healthy | `PASS`, `REUSE`/`REUSED`, `EXTENSIBLE` |
| cyan | something new | `CREATE`/`CREATED`, `RESERVE`, `TODO`, `DRY-RUN` |
| yellow | a resource the user owns is modified, or money | `WARN`, `APPEND`/`APPENDED`, `MODIFY`, `COST`, `IRREVERSIBLE` |
| red | actually wrong | `FAIL`, a non-`EXTENSIBLE` deployment |
| dim | structure and asides | rules, headers, "not checked" |

All five scripts carry the same preamble and degrade to plain text off a tty,
under `NO_COLOR`, or with `TERM=dumb`. **The tty test is on fd 2**, because the
scripts log to stderr — testing stdout would colour a piped run and leave an
interactive one plain, which is exactly backwards.

Tables are box-drawn with a header rule. Reuse the same table shape when the
same information recurs: the plan table and the completion table differ only in
their last column, and that is deliberate — the reader learned the shape once.

When you render a plan, a status summary or a completion report yourself rather
than running a script, follow the same scheme. A report that looks different
from the one the script printed two minutes earlier reads as a different tool.

**Never emit raw HTML in chat output** — no `<sub>`, `<br>`, `<span>` or
similar. Terminals show the tag literally and it reads as a rendering bug.
Use plain text or markdown; if something needs a subscript or a line break
inside a table cell, restructure it instead.

## Assessing an existing setup

`scripts/assess_integration.sh` is the read-only verb. Use it when the user asks how
things are running, when something is broken, and before planning any change.

**Say that it changes nothing — before running it, and again when reporting.**
It inspects and never writes: nothing is created, modified or deleted, so it is
safe to run against production. State that explicitly rather than leaving it to
be inferred from the word "assessment". Someone who has just been told their
setup may be misconfigured will not assume that a diagnostic is non-destructive,
and on a production gateway that doubt is enough to stall the whole
conversation.

Output is two tables. **Lead with the first one when reporting to the user.**

A **Setup Status Summary** rolls the whole run into six category rows, where
the Status column carries a *value* rather than only a verdict and the Details
column states the *consequence*:

```
┌─ Setup Status Summary ────────────────────────────────────────────────────────────────────────
 CATEGORY          STATUS                   DETAILS
 Overall Health    OK, WITH NOTES           19 PASS, 0 FAIL, 1 WARN, 0 TODO -- built and healthy
 Proxy             EXTENSIBLE rev 4         agent-gateway-governance on agent-gateway-govern
 Enforcement       METER + ARMOR:ENFORCE    Model Armor DOES refuse a matching request (400); quotas count only
 Caching           ON  (e2-standard-2 x1)   deployed index 5589640038682984448 -- BILLING per node-hour
 Governed Shapes   1                        :generateContent
 Callout Path      Verified                 PSC 10.138.0.9 ACCEPTED, zone resolves the hostname
 AuthZ Wiring      Verified                 <gateway>-apigee-governance-policy
────────────────────────────────────────────────────────────────────────────────────────────────
```

That block is copied from a real run, not composed. Keep it that way when the
output changes: a documented example that has drifted from the tool is worse
than none, because a reader diffs their output against it and concludes
something is wrong.

**Read the Proxy row first whenever the complaint is that governance does not
seem to be doing anything.** Its deployment type settles that question on its
own: `EXTENSIBLE` means the gateway is able to call the proxy, `STANDARD` means
it never will. A `STANDARD` deployment is not invoked at all — no error, no
transaction, nothing in a debug session — so every other check in the run can
pass while not one request is governed. Confirm `EXTENSIBLE` before
investigating anything downstream of it; `STANDARD` makes the rest moot.

**The Enforcement row is the one to read out loud.** It answers the question a
reader cannot otherwise get without opening a feature file: does anything here
block a request? `METER ONLY` means no. `METER + ARMOR` means Model Armor is
deployed at `modelArmor.mode: ENFORCE`, where the policy is
`continueOnError: false` and fails **closed**. `METER + ARMOR:DRY_RUN` means it
is deployed in observe-only mode — it evaluates and logs, and blocks nothing.
Read the mode, not just the presence of the policy.

**Report that row as it stands. Do not revise it by reading the bundle.** The
script derives Enforcement from the deployed revision, not from config, and it
is the answer. Finding `LLMTokenQuota` policies in the bundle and concluding
the proxy enforces is wrong: **the shipped quotas are `CountOnly`, and a
`CountOnly` quota counts without ever refusing.** The enforcing half is a
separate request-flow `EnforceOnly` policy that only exists if
`feature-token-enforce.yaml` was added — which is exactly what the script
already tested. So:

| Row says | Answer | Never say |
| --- | --- | --- |
| `METER ONLY` | nothing blocks — the quotas are `CountOnly`, so they count without ever refusing | that quotas or Model Armor can refuse here |
| `METER + QUOTA LIMIT` | the token budget is enforced, one request late | that it refuses the turn that crosses the limit |
| `METER + ARMOR:ENFORCE` | Model Armor refuses a matching request (400) | that the quotas also refuse, unless the row says so |
| `METER + ARMOR:DRY_RUN` | nothing blocks — Model Armor evaluates and logs | that Model Armor is protecting traffic |

Give the **reason**, not just the value — even in a one-line answer. "Nothing
blocks: the quotas are CountOnly" is one line and tells the reader why; "no"
makes them run the assessment again themselves.

If you believe the row is wrong, say so **and** say the row disagrees. Quietly
upgrading `METER ONLY` to `METER + QUOTA LIMIT` reports a protection the user
does not have, which is the worst failure this assessment can produce. Never
report a mode or status for a resource the assessment did not find.

**Four statuses, and TODO vs FAIL is the one that matters.** `TODO` means this
skill creates the resource and has not yet — the expected state of a greenfield
project, not a defect. `FAIL` means something no build step will resolve: a
missing user prerequisite, or a conflict. `SKIP` means the check did not run,
either because a flag was not passed or because its precondition is still a
`TODO`. Never report a never-built setup as a wall of failures; say `NOT BUILT`
or `PARTIALLY BUILT` and read the TODOs as the build plan they are. The exit
status follows the same rule — only a real `FAIL` is non-zero.

A bare `--project --region --gateway` invocation **assumes the documented
default names** for the environment, envgroup, proxy and hostname, and prints
which ones it assumed. If the setup under test uses different names, pass the
matching flags or every Apigee row will read as not-yet-built.

Then a **Checks** table, one row per resource with PASS, FAIL, WARN, TODO or
SKIP, and a
count. Read the FAILs top-down and fix in that order: a gateway with no route
into the VPC makes every check below it meaningless, so fixing a lower one
first wastes the cycle.

`--json` carries both: `summary`, `rollup`, and `checks`.

Two things the rollup deliberately does not do. It does not replace the Checks
table — a category row cannot tell you *which* of nineteen checks failed. And
it never infers: Enforcement and the feature flags are read off the deployed
revision's policy list, not off the config the user handed in, so it reports
what is actually running.

WARN is not a defect. The two that matter:

- **Another CONTENT_AUTHZ policy on the same gateway.** Coexistence is
  expected — a gateway acquires one automatically when agents are registered,
  and other governance products add their own. A `REQUEST_AUTHZ` policy
  alongside ours is a
  different phase and chains cleanly. Two `CONTENT_AUTHZ` policies is the one
  ambiguous case: **precedence between them is undefined, and there is no
  tie-break rule to fall back on — not alphabetical, not creation order, not a
  priority field.** Say it is undefined; never guess an order. They cannot be
  merged either, since an AuthzPolicy takes a single custom provider. Full
  answer, including the wrong rules people reach for:
  `references/gotchas.md`, Agent Gateway.
- **DNS peering that does not cover your hostname.** Peering is per-domain, so
  this is an append, not a conflict.

Exit status is 0 when there are no FAILs, 1 otherwise, so it is usable as a gate
in a script.

# Two modes: dev and prod

The same skill, the same schema, two entry points. **Dev mode writes
`apigee-agent-gateway-governance.yaml`; prod mode reads it.** What dev mode emits must be consumable by
prod mode unchanged — one schema, or the determinism prod mode promises is not
real.

## Choosing the mode

Do not ask the user which mode they want. Decide it:

| Situation | Mode |
| --- | --- |
| An input file exists and the user points at it | **prod** |
| The user asks for a specific file to be applied | **prod** |
| No input file, and the user describes an outcome | **dev** |
| User says "deterministic", "production", "check this in" | **prod** |

State which mode you picked and why, in one line, before doing anything.

---

# Dev mode

For an FDE or a customer meeting this for the first time. They do not know the
schema exists, and **they should not see YAML during setup.**

## What you ask for

Only what cannot be defaulted or discovered:

- `project`, `region` — region must match the Apigee runtime instance
- `gateway.name` — must already exist; list them rather than asking them to type one
- `network.vpc`, `network.subnet` — must be the VPC the gateway egresses into

Everything else gets a default (below). Discover what you can with `gcloud`
before asking: if the project has exactly one Agent Gateway in the region, name
it and confirm rather than asking.

## Defaults

Apply these silently. Show them in the plan; do not interrogate the user
field by field.

| Field | Default | Note |
| --- | --- | --- |
| `apigee.org` | = `project` | |
| `apigee.environment` | `agent-gateway-govern` | created if absent, dedicated to this proxy |
| `apigee.envgroup` | `agent-gateway-govern-group` | |
| `apigee.hostname` | `agent-gateway-callout.internal.<project>.local` | private to the VPC; nothing resolves it publicly |
| `apigee.proxy` | `agent-gateway-governance` | |
| `network.networkAttachment` | `agent-gateway-egress-attachment` | created if absent |
| `network.dns.zone` | `agent-gateway-callout-zone` | |
| `network.dns.domain` | `internal.<project>.local.` | parent of the hostname, trailing dot |
| `gateway.manageNetworkConfig` | `true` | prints a diff and waits for confirmation |
| `gateway.matchPaths` | `[":generateContent", "/chat/completions"]` | **two shapes**, matching the template's `LLM_URI_MATCH` default and `assets/apigee-agent-gateway-governance.example.yaml`. Drop the second entry for a Gemini-only agent — but then also drop the matching clause from `LLM_URI_MATCH` in every feature that declares it, or the two disagree. If the semantic cache is on, two shapes triggers the known-issue warning |
| `gateway.timeout` | `5s` | |
| `identity.enabled` | `true` | |
| `identity.defaultClientId` | `anonymous` | |
| `tokenMetering.enabled` | `true` | |
| `tokenMetering.interval` / `timeUnit` | `1` / `hour` | |
| `tokenMetering.models` | pro 10000, flash 40000, other 40000 | per-model buckets |
| `tokenMetering.mode` | `COUNT_ONLY` | `ENFORCE` refuses an over-budget caller on its **next** request (429); adds `feature-token-enforce.yaml` |
| `modelArmor.enabled` | `false` | opt-in, see below |
| `modelArmor.template` | **none** | required when enabled; refuse rather than invent one |
| `modelArmor.mode` | `ENFORCE` | `DRY_RUN` evaluates and logs but does not block |
| `semanticCache.enabled` | `false` | opt-in, see below |
| `semanticCache.deployedIndexId` | `agent_gateway_llm_cache` | underscores only — hyphens are rejected |
| `semanticCache` index display name | `agent-gateway-llm-cache-index` | `--index` for `ensure_vector_search.sh` |
| `semanticCache` endpoint display name | `agent-gateway-llm-cache-endpoint` | `--endpoint` for the same script |

**Two fields in the contract change the proxy's feature list rather than a
parameter**, and they are the only ones that do. Resolve them before building:

| Field | Value | Effect on the template's `features:` |
| --- | --- | --- |
| `tokenMetering.mode` | `COUNT_ONLY` | nothing added — metering only |
| | `ENFORCE` | add `feature-token-enforce.yaml` |
| `modelArmor.enabled` | `false` | nothing added |
| | `true` | add `feature-model-armor.yaml`; `mode` then sets `MA_CONTINUE_ON_ERROR` |
| `semanticCache.enabled` | `true` | add `feature-semantic-cache.yaml` |

`modelArmor.mode` is a **parameter** on an already-present feature, so toggling
it edits `MA_CONTINUE_ON_ERROR`. `tokenMetering.mode` is a **feature
membership** switch, because enforcement is a separate set of policies on a
different flow. Same shape in the contract, different mechanism underneath —
worth knowing when a mode change does not appear to take: for Model Armor
check the parameter in `feature-model-armor.yaml`, for metering check the
feature list.

Both `*_TOKEN_LIMIT` sets must agree between `feature-token-metering.yaml` and
`feature-token-enforce.yaml`, or enforcement refuses at a different threshold
than counting reports against. `compile_check.py` fails on the mismatch.

**Names are chosen so someone who finds these resources cold can tell what they
are for.** Inside Apigee the prefix is `agent-gateway-`, because what is unusual
about the proxy is that it serves an Agent Gateway. On the gateway side the
pattern is `<gateway>-apigee-llm-*`, because there what is unusual is that the
gateway calls Apigee. Do not name anything after `ext-proc`: that is the
mechanism, not the purpose, and it tells a reader nothing about what the
resource governs.

## Start with two features, not four

Identity and token metering only. They need no extra Google API, no service
account, and no provisioned resource, so the first run reaches a working,
verifiable state fast.

**Offer Model Armor and semantic cache only after the base setup verifies** —
after a real agent turn has shown up in a debug session. Enabling them before
the base works means a failure has two possible causes.

When the user asks for either, state what it costs before doing it:

**Model Armor** — needs a Model Armor template (ask for the name; there is no
sensible default) and `roles/modelarmor.user` on the deployment service
account. No standing cost. Adds one inline call per request.

**Model Armor has an observe-only mode.** `modelArmor.mode: DRY_RUN` keeps the
scan running and the verdict in the trace while swallowing the fault, so a
turn is never refused.

It is one of two capabilities with an observe-versus-refuse switch, and they
default in opposite directions on purpose:

| | observe | refuse | default |
| --- | --- | --- | --- |
| `modelArmor.mode` | `DRY_RUN` | `ENFORCE` | **`ENFORCE`** |
| `tokenMetering.mode` | `COUNT_ONLY` | `ENFORCE` | **`COUNT_ONLY`** |

A safety control that silently does not protect is worse than one that
visibly blocks, so Model Armor ships enforcing. A cost control that
unexpectedly refuses production traffic is worse than one that reports, so
metering ships counting. Do not describe either as "the only one with a
mode".
`ENFORCE` is the default and the shipped position: a security control that
silently does not protect is worse than one that visibly blocks. Offer DRY_RUN
when someone enables Model Armor on a proxy already carrying live traffic, so
they can see what a template *would* have blocked first. It is not an on/off
switch — disabling the feature removes the evaluation entirely. Toggling is a
redeploy, roughly two minutes.

**Semantic cache** — needs Vertex AI Vector Search. Say all three of these:

- The index endpoint deploy alone takes **about 34 minutes**.
- A deployed index **bills per node-hour for as long as it is deployed, with
  or without traffic.** It is the only thing in this skill that bills
  continuously.
- Turning it off later means undeploying the index, not just editing the YAML.
  Undeploying underneath a live proxy faults every request, so the teardown has
  an order.

Get explicit confirmation on the cost point. Do not infer it from "yes, enable
caching".

**This is the one approval you may not grant on the user's behalf.** Ask, then
stop and wait for an answer. "Enable semantic caching" is a request for the
feature, not consent to a continuously-billing resource, and the standing
*one approval, then execute to the end* rule does not cover it — that rule is
about not interrupting an **already-approved** plan, and the cost point is what
is being approved. If no answer comes, the correct outcome is to stop with the
cost stated and nothing provisioned. Never record this as assumed, implied or
automatic confirmation: a 34-minute deploy that bills per node-hour is not
recoverable by saying sorry afterwards.

## Discover before you plan

**Run `scripts/assess_integration.sh` first, in both modes.** It is read-only and
changes nothing, so it is safe before the user has agreed to anything. It is
also the only honest way to say what already exists — guessing produces a plan
that creates a second copy of something the project already has.

```bash
scripts/assess_integration.sh --project P --region R --gateway G \
  [--env E --envgroup EG --hostname H --proxy PX --vpc V --subnet S] [--json]
```

`--json` is the form the plan reads. Every check maps to a plan row.

This matters most when another extension is already on the gateway. Another
governance product may bring its own network attachment, DNS zone, PSC
endpoint and authz policy. Some of that is shareable and some is not, and the
split is not obvious:

| Resource | With an existing extension present |
| --- | --- |
| VPC, subnet | **REUSE** |
| Gateway egress `networkAttachment` | **REUSE** — a route into the VPC, not to a service |
| Gateway `dnsPeeringConfig` | **APPEND** a domain — peering is per-domain |
| Private DNS zone | REUSE only if its domain is a parent of your hostname |
| PSC IP + forwarding rule | **CREATE** — must target the *Apigee* service attachment |
| AuthzExtension | **CREATE** — points at your hostname |
| AuthzPolicy | **CREATE** — one custom provider per policy, cannot merge |

Say which of these you found, not which you assumed.

## The plan

Before executing anything, print the plan and get approval. One line per step,
each with its duration. Do not start until they say go.

### Confirm everything up front

**This does not mean "discover until you are certain". It means the plan
carries every question, and you still stop at the plan.**

The sequence is fixed and short: run assess **once**, write the plan, print it,
**stop**. Do not re-run assess to resolve a detail, do not probe resources one
by one to firm up an estimate, and do not begin any step to find out whether it
would work. An unknown that assess did not answer belongs in the plan as an
unknown, with what you will do when you hit it. A plan printed from one
assessment and one pass of reasoning is the deliverable; a half-built
environment produced while "gathering decisions" is not.

**One approval, then execute to the end.** Do not stop halfway to ask for
something that was knowable at planning time — a build that pauses at minute 12
is worse than one that asked at minute zero, because the user has stopped
watching and the half-built state is the awkward one to abandon.

Three things need a human answer, and assess already tells you which of them
apply before you print the plan. "A human answer" means one the user actually
gave: none of the three may be self-granted, inferred from the original
request, or recorded as assumed or automatic confirmation. Ask them **at
planning time**, which is what makes the single-approval rule above work —
they are the content of that approval, not an interruption to it.

| Decision | Ask when | Why it cannot wait |
| --- | --- | --- |
| Attach gateway egress | `networkConfig` absent | One-way, and pins **all** the gateway's egress into that VPC — agents already running can lose access to Google APIs |
| Vector Search cost | `semanticCache.enabled` | Bills per node-hour from deploy, ~34 min to stand up, and undeploying underneath a live proxy faults every request |
| Enforcement, not just metering | user wants a budget | Changes what the proxy does to traffic; offer it, do not assume it |

Put each one in the plan with its consequence spelled out, take a single
approval covering all of them, and then run uninterrupted. If the user declines
one, say what the run produces without it rather than stopping — declining
Vector Search is a smaller setup, not a failed one.

The only legitimate mid-run stop is something assess could not have known: a
quota refusal, a permission the project turns out not to have, an API that
errors. Those are reports, not requests for permission.

**Every resource row carries an action, and the action comes from assess**, not
from a default. `REUSE` rows are the ones the user cares about — they are what
makes adding Apigee to an existing setup cheap.

Render it as a real table, grouped by leg, with the action column aligned and
colour-coded the same way `assess_integration.sh` colours its statuses — green
`REUSE` (nothing happens to it), cyan `CREATE` / `RESERVE` (new, and billable
where marked), yellow `APPEND` / `PATCH` (an existing resource the user owns is
modified). A flat 14-row monospace list is the thing being reviewed for consent,
so it has to be skimmable: the reader's question is "what are you touching that
already exists", and grouping plus colour answers it at a glance where an
unbroken column of names does not.

```
┌─ Plan · resources ────────────────────────────────────────────────────────────────────────────

  GATEWAY LEG                                                          ACTION
  ─────────────────────────────────────────────────────────────────── ───────
  VPC network                 default                                  REUSE
  Agent subnet                default (10.142.0.0/20)                  REUSE
  Gateway network attachment  agent-gateway-egress-attachment          REUSE
  Gateway DNS peering         internal.acme.local.                     APPEND ←modifies

  APIGEE LEG                                                           ACTION
  ─────────────────────────────────────────────────────────────────── ───────
  Apigee environment          agent-gateway-govern                     CREATE
  Environment group           agent-gateway-govern-group               CREATE
  API proxy                   agent-gateway-governance                 CREATE

  CALLOUT PATH                                                         ACTION
  ─────────────────────────────────────────────────────────────────── ───────
  PSC static IP               agent-gateway-callout-psc-ip             RESERVE
  PSC forwarding rule         agent-gateway-callout-psc-endpoint       CREATE
  Private DNS zone            agent-gateway-callout-zone               REUSE
  DNS A record                agent-gateway-callout.internal.acme.local CREATE
  AuthzExtension              <gateway>-apigee-governance-extension    CREATE
  AuthzPolicy                 <gateway>-apigee-governance-policy       CREATE

  3 REUSE · 9 CREATE/RESERVE · 1 APPEND (modifies a resource you already own)
```

The footer line is the point of the table. Lead with it when you present the
plan: the count of things being modified is what the user is actually
approving.

**Gateway DNS peering is never `REUSE`.** It is the one row people get wrong,
because an existing peering config looks like something to reuse. Peering is
**per-domain**: an existing config covering another domain does not cover
yours, so your domain is **appended** to it. That makes the row `APPEND`, and
`APPEND` means the gateway — a resource the user already owns — is modified.
Marking it `REUSE` hides a modification inside a row that reads as free, which
is the one mistake this table exists to prevent.

Then the ordered steps. Keep it to one line each — a step list is scanned, not
read, and prose beside a duration is what makes a plan look longer than the
work.

```
┌─ Plan · steps ────────────────────────────────────────────────────────────────────────────────
  LLM governance on my-agent-gateway                         acme-prod · us-east1

  #  STEP                                     TIME   NOTE
  ─  ───────────────────────────────────────  ─────  ──────────────────────
  1  Enable APIs                               ~1m
  2  Environment + attach to instance          ~4m   env LOCKED while running
  3  Envgroup on the callout hostname          ~1m
  4  Gateway egress attachment + DNS peering   ~2m   modifies your gateway
  5  PSC endpoint + private DNS A record       ~3m
  6  Build and deploy the proxy                ~2m   must report EXTENSIBLE
  7  AuthzExtension, then AuthzPolicy          ~2m
  8  Debug session, verify a live turn         ~2m
                                              ─────
                                              ~20m   step 2 is most of it

  ON   identity · token metering
  OFF  Model Armor · semantic cache · enforcement   (offered after step 8)
  OUT  apigee-agent-gateway-governance.yaml — commit this
```

Colour the `NOTE` column the same way as the resource table: yellow for a row
that modifies something the user owns, plain otherwise.

**The `OUT` line is required.** The run ends with a file to commit and the user
has no idea one is coming otherwise; it is the whole bridge to re-running this
reproducibly. Durations are measured, not guessed — quote these. If a step runs
long say so rather than going quiet, because several of them look hung when
they are merely slow.

**Step 2 is not optional detail.** Whatever shape the plan takes — the full
table, a condensed list, a sentence — it must state that creating and attaching
the environment takes **several minutes (~4m)** and **locks the environment
while it runs**. That is the longest step, it is most of the ~20m total, and
the lock is the part the user cannot work around once it starts. Dropping the
`NOTE` cell to shorten the table drops the one thing they needed before
approving, so if the table is abbreviated, say it in prose instead. The same
goes for the other two `NOTE` cells: step 4 modifies the user's own gateway,
and step 6 must come up `EXTENSIBLE`.

## What dev mode produces

**Close with the same resource table, now showing what actually happened.**
The plan said what you intended; this says what exists. Same rows, same
grouping, same colours — only the action column changes, from intent to
outcome, with the elapsed time beside it. Reusing the shape is the point: the
reader already learned to read it ten minutes ago, and a diff between the two
tables is the whole report.

```
┌─ Done · LLM governance on my-agent-gateway ───────────────────────────────────────────────────
  acme-prod · us-east1                                              elapsed 18m42s

  GATEWAY LEG                                                      OUTCOME
  ─────────────────────────────────────────────────────────────── ─────────
  VPC network                 default                              REUSED
  Agent subnet                default (10.142.0.0/20)              REUSED
  Gateway network attachment  agent-gateway-egress-attachment      REUSED
  Gateway DNS peering         internal.acme.local.                 APPENDED

  APIGEE LEG                                                       OUTCOME
  ─────────────────────────────────────────────────────────────── ─────────
  Apigee environment          agent-gateway-govern                 CREATED
  Environment group           agent-gateway-govern-group           CREATED
  API proxy                   agent-gateway-governance  rev 1      DEPLOYED  EXTENSIBLE

  CALLOUT PATH                                                     OUTCOME
  ─────────────────────────────────────────────────────────────── ─────────
  PSC endpoint                10.142.0.42                          CREATED   ACCEPTED
  Private DNS zone            agent-gateway-callout-zone           REUSED
  DNS A record                agent-gateway-callout.internal…      CREATED
  AuthzExtension              my-agent-gateway-apigee-…-extension  CREATED
  AuthzPolicy                 my-agent-gateway-apigee-…-policy     CREATED

  VERIFIED  1 transaction captured on a live turn · identity + tokens present
  OUT       apigee-agent-gateway-governance.yaml
```

Green for `REUSED`, cyan for `CREATED`/`DEPLOYED`, yellow for `APPENDED`.
Carry the second value where there is one — `EXTENSIBLE` and `ACCEPTED` are the
two that decide whether any of this works, and burying them in prose is how a
run that silently governs nothing still reads as a success.

Anything that did **not** happen gets a row too, with the reason. A completion
table that lists only successes is the same failure as an assessment that
reports only what it checked.

Then write `apigee-agent-gateway-governance.yaml` into the working directory in the
schema `assets/apigee-agent-gateway-governance.example.yaml` documents, and show it to the user *then*
— as the handoff, not as an input:

> Everything above is captured in `apigee-agent-gateway-governance.yaml`. Commit it. From here you can
> change governance by editing that file and re-running, and the skill will
> reconcile to it — no conversation needed.

That sentence is the bridge to prod mode. It is the only point in dev mode
where the user sees YAML.

Emit exactly this shape — the same keys `assets/apigee-agent-gateway-governance.example.yaml`
documents. Prod mode has to be able to read back what dev mode wrote, unchanged,
so the **key set** must match with no drift in either direction.

**Carry a short comment header and a one-line comment on each non-obvious
field.** Not the example file's full explanations — a trimmed set. This file
gets committed and then read months later by someone who was not in the
conversation, and a bare key like `manageNetworkConfig: true` or a `matchPaths`
suffix list tells them nothing about what it controls or what breaks if they
change it. Comments cost nothing: they do not affect parsing, and the key-set
diff against the example ignores them.

What earns a comment: anything whose value was a decision (the match paths, the
feature toggles, `manageNetworkConfig`), anything with a non-obvious format (a
suffix rather than a path, a project number rather than an ID), and the header,
which should say what the file is, that it is the input to prod mode, and the
date and gateway it was generated against. What does not: `project`, `region`,
and anything self-describing.

The example file remains the full reference; this is the trimmed travelling
copy.


```yaml
apiVersion: apigee.googleapis.com/v1alpha1
kind: AgentGatewayGovernance
metadata:
  name: agent-gateway-governance
  description: Generated by apigee-agent-gateway-governance on <date>.
spec:
  project: <project>
  region: <region>
  apigee:
    org: <project>
    environment: agent-gateway-govern
    envgroup: agent-gateway-govern-group
    hostname: agent-gateway-callout.internal.<project>.local
    proxy: agent-gateway-governance
    deploymentServiceAccount: ""        # required once modelArmor or semanticCache is on
  network:
    vpc: <vpc>
    subnet: <subnet>
    networkAttachment: agent-gateway-egress-attachment
    dns:
      zone: agent-gateway-callout-zone
      domain: internal.<project>.local.
      record: agent-gateway-callout.internal.<project>.local   # must equal apigee.hostname
  gateway:
    name: <gateway>
    manageNetworkConfig: true
    matchPaths:
      - ":generateContent"
      - "/chat/completions"
    timeout: 5s
  features:
    identity:
      enabled: true
      defaultClientId: anonymous
    tokenMetering:
      enabled: true
      mode: COUNT_ONLY
      interval: 1
      timeUnit: hour
      models:
        - bucket: gemini-pro
          limit: 10000
        - bucket: gemini-flash
          limit: 40000
        - bucket: other
          limit: 40000
    modelArmor:
      enabled: false
      mode: ENFORCE
      template: ""
    semanticCache:
      enabled: false
      threshold: 0.95
      ttlSeconds: 60
      embeddingsModel: text-embedding-005
      deployedIndexId: agent_gateway_llm_cache
      indexEndpointId: ""
      indexId: ""
```

Write the values you actually used, not the placeholders. If the user enabled
Model Armor or the cache during the session, write them `enabled: true` with
the values that were provisioned — including `indexId` and `indexEndpointId`,
which `scripts/ensure_vector_search.sh` prints. A file that says `false` for a
feature that is live would make the next prod-mode run tear it down.

---

# Prod mode

The input file is the contract. The skill reconciles the setup to it.

## Hard refusal

**Refuse to run — do not improvise a config — when any of these hold:**

- No input file was supplied or found.
- `apiVersion` is not `apigee.googleapis.com/v1alpha1`, or `kind` is not
  `AgentGatewayGovernance`.
- A required field under `spec.project`, `spec.region`, `spec.apigee` or
  `spec.gateway` is missing or empty.
- A feature is enabled whose own required fields are absent — `modelArmor`
  without `template`, `semanticCache` without `deployedIndexId`.

Say which field is wrong and stop. Do not fall back to dev mode and do not
substitute a default: silently inventing a value in prod mode destroys the
guarantee the file exists to provide.

Offer the fix as a diff against their file, and let them apply it.

## Reconcile, don't re-create

Everything in the workflow is idempotent and safe to re-run. Re-running against
an unchanged file should converge and report no change.

Run the plan step (above) in prod mode too — `scripts/deploy_proxy.sh` has
`--dry-run`, so the plan costs nothing and catches a bad file before it touches
the org.

---

# Interlocks

These hold in **both** modes. They are refusals, not warnings, except where
stated — each one is a failure that produces no error at runtime.

**Semantic cache with more than one wire shape — warn, then build it.** This is
the one interlock that is a warning rather than a refusal, in both directions,
because the defect is upstream and temporary.

**Trigger condition: the cache is being enabled, full stop.** Not only when
`matchPaths` has more than one entry. Do not raise it when describing what the
skill can do or when the cache is off — a caveat about a configuration the user
has not chosen is noise — but a single model behind a single wire shape does
**not** make the cache safe, so do not treat one shape as the all-clear.

The cache key is the embedding of the prompt and nothing else: no caller, no
model, no wire shape, no tenant.

The consequence that applies to **every** cache deployment is that a hit
crosses caller boundaries. Two callers whose prompts are merely similar share
an answer, so anything caller-specific is served from whoever asked first. A
gateway normally has several callers, and identity is on by default, so this is
the common configuration rather than an edge case. `agw.client_id` is available
and the cache policies accept no discriminator, so it cannot be scoped away.

Two further effects once more than one model answers here. Cross-shape the
second caller gets a body in the wrong format as an **empty HTTP 200** — a
success with no content, which reads as the agent breaking. Same-shape is
quieter and worse: the body parses perfectly and the only tell is
`model_version` in the payload.

Build the cache anyway when asked, in all three directions:

- `semanticCache.enabled: true` at all → **warn and proceed**, naming the
  cross-caller exposure.
- `semanticCache.enabled: true` while `gateway.matchPaths` has more than one
  entry → **warn and proceed**, adding the wrong-model effects.
- Adding a second entry to `matchPaths` while the cache is enabled → **warn and
  proceed**.

The warning is not optional and must name the failure, not just gesture at it.
Emit it at plan time and again in the summary, in both modes:

> ⚠️ Known issue: the semantic cache keys on the prompt embedding alone — no
> caller, no model, no wire shape. **A hit is shared across callers**: two
> callers whose prompts are merely similar get the same answer, so anything
> caller-specific is served from whoever asked first. Enable it only where
> every caller may see every other caller's answer to the same question. One
> model behind one wire shape does not make this safe.
> With more than one wire shape a cached answer can also reach the wrong
> model's caller — an empty HTTP 200 across shapes, or a wrong-model body
> within one. The cross-shape case comes back as **success, not an error**: a
> 200 carrying no content, which reads as the agent itself being broken rather
> than as a cache fault, so it is looked for in the wrong place.
> Upstream fix expected; until it lands, treat cache hits as unverified.

Record it as a known issue in `apigee-agent-gateway-governance.yaml` whenever
dev mode writes a config with the cache on, so the next reader of the contract
sees it too.

**Model Armor without `feature-normalize`** — refuse. Model Armor reads
`agw.user_prompt`, which normalize sets at priority 15. Without it Model Armor
fails **closed** on every matching request. Normalize is in the base template,
so this only arises if someone has edited the feature list.

**A feature that calls a Google API without `deploymentServiceAccount`** —
refuse before deploying, not after. Model Armor and semantic cache both need
one; the deploy fails with `MISSING_SERVICE_ACCOUNT` otherwise, which reads as
a permissions problem rather than a missing field.

**Token metering does not gate on its own, and enforcement is a separate
feature.** The `CountOnly` quotas in `feature-token-metering.yaml` observe and
never block. To turn a budget into a limit, add
`assets/feature-token-enforce.yaml`, which puts `EnforceOnly` policies on the
request path under the same `SharedName`. Never improvise request-path
enforcement by making the metering quotas blocking: a blocking quota in the
response flow cannot withhold a response already on the wire, and it stops
counting the request that broke the limit. State that enforcement is one
request late by construction — the cost of a turn does not exist until the
model has answered, so the turn that crosses the limit completes and the
caller's next request is refused. See `gotchas.md`.
