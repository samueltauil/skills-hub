# Recipes

Each recipe is an **AFT feature**, not a separate setup procedure. Enable one
by adding its file to the template's `features` list and recompiling:

```yaml
features:
  - feature-identity.yaml
  - feature-token-metering.yaml
  - feature-model-armor.yaml      # add this
```

```bash
python3 scripts/compile_check.py assets/apigee-proxy-template.yaml  # offline; needs PyYAML
gcloud apigee apis import organizations/$ORG/apis/$PROXY \
  --from-template=assets/apigee-proxy-template.yaml
```

Features merge by `priority`: identity 10, token enforcement 12, normalize 15,
Model Armor 20, semantic cache 30, metering 50. Steps land in that order within
each flow.

**Every recipe must be gated.** A fail-closed policy with no condition kills the
agent's turn on the first call that carries no prompt. How exposed you are
depends on the AuthzPolicy: a suffix list of model-call paths routes only those
(measured with `:generateContent` alone), but widen it and the ext-proc sees all
agent egress — 12 calls for one measured turn, 11 of them promptless. Gate regardless, so the
policy stays safe to widen.

## Contents

-   [Status](#status): lines 37-98
-   [E1 — Model Armor](#e1-model-armor): lines 99-113
-   [E2 — Semantic cache](#e2-semantic-cache): lines 114-178
-   [E3 — ServiceCallout](#e3-servicecallout): lines 179-184

## Status

The `Live traffic` column is the one that decides risk. "No" does not mean
broken; it means nothing has proved its runtime behaviour, which is a
different claim from "it compiles".

| Recipe | Feature file | Compiles | Live traffic |
| --- | --- | --- | --- |
| Identity | `feature-identity.yaml` | yes | **yes** — JWT verified, `agw.client_id` set on a real turn |
| Token metering | `feature-token-metering.yaml` | yes | **yes** — per-model counters moved on real turns |
| E1 Model Armor | `feature-model-armor.yaml` | yes | **yes, thinly** — injections refused through ENFORCE; one benign prompt passed `NO_MATCH_FOUND`. No false-positive rate |
| E2 Semantic cache | `feature-semantic-cache.yaml` | yes | **yes** — miss/hit measured end to end, see below |
| Token enforcement | `feature-token-enforce.yaml` | yes | **yes** — over-budget caller refused with 429 on live gateway traffic, model never called (`used.count` 1086 vs `allowed.count` 500) |
| E3 ServiceCallout | — | — | deliberately not authored, see below |

**E1 is still the one to be careful with**, but for a narrower reason than
before. It now has live evidence in both directions: injections were refused
through ENFORCE, and one ordinary prompt (`"name a planet"`) returned
`filterMatchState = NO_MATCH_FOUND` and completed normally, so routine traffic
does survive `MEDIUM_AND_ABOVE`. One benign sample is not a false-positive
rate. It remains the only recipe that fails **closed**, so on a proxy already
serving turns recommend `DRY_RUN` first and say why: the unknown is not
whether it works, it is how often it refuses something it should not.

**E2 measured live** — one prompt sent twice inside the 60s TTL:

| | miss | hit |
| --- | --- | --- |
| proxy-side elapsed | 2410 ms | **375 ms** |
| `cache_hit` | false | true |
| `nearest_neighbor_measure` | — | 0.999999 (threshold 0.95) |
| `SCP-populate` upsert | ran | **skipped** |
| flash quota counter | moved | **absent — quota skipped** |
| Model Armor | ran | **ran** |

Four documented traps confirmed correct by that pair: populate is skipped on a
hit, so the pre-namespaced `cache_hit` condition really does resolve (the
documented `semanticcache.lookup.*` form would have failed open and
re-upserted); metering does not double-count, because although
`metering-JS-extract-model` runs ungated and did extract 188 tokens from the
replayed body, every `LTQ` step was skipped; the matched key equals the
`datapointId` the miss wrote, so the round trip is real rather than a
coincidental neighbour; and **a hit still pays for Model Armor**, which runs
at priority 20 before the lookup at 30. The cache saves the model call, not
the scan — the 375 ms includes the scan, an embeddings call and
`findNeighbors`.

All six compile together: 16 policies and 22 bundle entries, steps ordered
identity → enforcement → normalize → Model Armor → cache lookup in
`PreFlow/Request`, and cache populate → metering in `PostFlow/Response`.

The **base** proxy — identity plus token metering — is deployed on a live org
and verified `EXTENSIBLE`.

**Verification status is per-recipe, and the table below is the only source of
truth for it.** Do not generalise from this paragraph; an earlier version of it
claimed none of the optional recipes had seen live traffic, which contradicted
E2's own live measurements twenty lines later. Where a recipe says
"compile-verified only", that means the check proved structure and nothing
proved runtime behaviour — which is the distinction that matters for Model
Armor, the one recipe that fails **closed**.

## E1 — Model Armor

Authored. Screens the prompt before the model; blocks on a filter match. A
benign prompt passes; an unsafe one is stopped **before Gemini** and surfaces
as `400 … steps.sanitize.user.prompt.FilterMatched`.

Needs `roles/modelarmor.user` on the deployment SA and a deploy with
`?serviceAccount=`. `SanitizeModelResponse` is the response-path analogue, its
source being `$.candidates[-1].content.parts[-1].text`.

**It reads `agw.user_prompt`, not a JSONPath**, and that variable is set by
`feature-normalize.yaml` at priority 15. Enabling Model Armor without that
feature leaves the variable unset — and because the policy fails closed, the
result is HTTP 500 on every matching request rather than a skipped scan.

## E2 — Semantic cache

Authored and verified live. Two policies: `SemanticCacheLookup` in the Request
PreFlow, `SemanticCachePopulate` in the response phase.

Two things make this harder than it looks on a no-route proxy:

- **Populate must be gated on the cache-hit flag.** With no target endpoint the
  response flow runs on a hit too, so ungated populate re-embeds and re-upserts
  the answer it just served.
- **The flag is not the documented name.** Runtime emits
  `SemanticCacheLookup.<policy>.cache_hit`; the docs say
  `semanticcache.lookup.<policy>.cache_hit`, which never resolves — and an
  unresolved variable makes `!= true` true, so it fails open and looks exactly
  like the ungated bug.

When authoring this as a feature, the condition must be written
**pre-namespaced** (`SemanticCacheLookup.semanticcache-SCL-lookup.cache_hit`),
because the compiler does not rewrite policy-derived flow variables.

- **Metering double-counts on a hit unless you gate that too.** The quota reads
  the token count out of the replayed response and counts tokens the model
  never produced — measured, the counter moved by exactly the replayed answer's
  97 tokens. `feature-token-metering.yaml` carries the same cache-hit clause on
  **all three** quota steps. Enabling the cache without it silently inverts
  what the cache is for.
- **Populate must also be gated on `response.status.code = 200`.** The policy
  is status-blind: gated only on the hit flag it caches upstream errors too.
  Observed — a transient 429 written to the cache and then replayed **as HTTP
  200** to every identical prompt for the whole TTL, turning a momentary blip
  into a persistent wrong answer that defeats status checking. Raised with the
  Apigee team; carry the gate regardless, it is the only defence today.

Measured on a live setup: cold 4743 ms versus 336 ms served from cache, with
the model never called. A second run on a different prompt measured 1396 ms
versus 382 ms — a 3.7x ratio.

**Measure proxy-side, from a debug session, not from the caller.** On that same
pair the client saw 15445 ms versus 13114 ms — a 15% difference
indistinguishable from noise, because agent session setup dominates the round
trip. Anyone timing the caller concludes the cache does nothing.

**A hit still pays for Model Armor.** Feature priority puts Model Armor (20)
ahead of the cache lookup (30), so the compiled request flow scans the prompt
before the cache is consulted. That order is the safer one — it stops a prompt
reaching a cached answer unscanned — but it means the floor on a hit is the
Model Armor latency, not zero.

**The cache reads `agw.user_prompt` too**, from the same priority-15 feature.
That is what lets one cache serve both wire shapes: `LLM_URI_MATCH` matches
`*generateContent*` and `*chat/completions*`, and the prompt is selected from
either body layout in JS. Verified — a repeat prompt hit across shapes.
Do not widen `LLM_URI_MATCH` without `feature-normalize` present; the same
condition arms Model Armor, which fails closed.

**Prerequisites are built by `scripts/ensure_vector_search.sh`**: the index
(width fixed by `embeddingsModel`, `STREAM_UPDATE`, both immutable), the
endpoint, and the deploy of one onto the other. `--yes` gated, idempotent and
resumable — resumable matters because the deploy step alone runs about 34
minutes. It is also the only part of this skill that bills continuously, per
node-hour for as long as the index stays deployed; the script prints the cost
note and the teardown order before asking. You also need
`roles/aiplatform.user` on the deployment service account, and
`<DeployedIndexID>` spelled all-caps.

## E3 — ServiceCallout

Deliberately not authored. `ServiceCallout` is on the Extension Processor
unsupported-policy list, yet it imports, deploys `EXTENSIBLE` and executes from
both flows. Docs and platform disagree; don't build on it until that is
resolved.
