---
name: docker-sandboxes-kits
description: >-
  Use this skill when authoring, verifying, publishing, or composing a Docker Sandboxes kit, even if the user just says they want to "add a tool to a sandbox agent", "package a CLI or agent as a kit", "publish a kit to a registry", or "give a mixin its own credentials and network access". Covers the v3 kit descriptor (`# syntax=docker/sandbox-kit:3`, `kind: workload` or `mixin`, typed capabilities, provides/requires, content recipes), building with docker buildx, checking with kit-tck and `sbx kit inspect`, composing onto a workload, referencing and pinning a kit from an `sbxenv.yaml` `agent:`/`kits:` entry, and publishing and signing. Legacy v2 `spec.yaml` kits are not covered; `sbx kit validate` is not a substitute for kit-tck conformance and runtime checks.
license: Apache-2.0
compatibility: Experimental. Needs docker buildx, kit-tck, and an sbx release with Kits v3 support (adapted from docker/sandbox-kit-spec at 4d932451613f8df89c8468e2bb7c5286882897ca; build/conformance tested 2026-11-02; authenticated inspect/validate and composition tested on sbx v0.50.1 with optional agent-context@2; sbxenv.yaml kit-reference rules sourced from sbx v0.51.0 docs, help, and earlier runtime records, not re-run here). Not the legacy docker sandbox wrapper. See references/sources.md.
---

# Docker Sandboxes: Kits (v3 descriptors)

## Overview

A **kit** extends a sandbox with a tool, an agent, credentials, or policy. In
v3 a kit is one OCI image: its layers are the content, and a manifest
annotation carries the **descriptor**, which says what the kit offers, what it
needs from the host as typed capability requests, and what it needs from
other kits. An engine that does not read the annotation runs it as an
ordinary image.

The source is a `<kit>.yaml` whose first line is
`# syntax=docker/sandbox-kit:3` with `schemaVersion: "3"`, usually beside a
`<kit>.dockerfile` content recipe. The kinds are `workload`, `mixin`, and
`set` (a list of other kits). Build and check with `docker buildx build`,
`kit-tck validate`, `sbx kit inspect`, and a real `sbx run` composition.

Scope and guardrails:

- **Legacy v2 `spec.yaml` kits (`schemaVersion: "2"`, `kind: sandbox`) are
  not covered here.** This is the skill's routing boundary, not a claim that
  v2 has been deprecated or removed. This skill neither authors nor debugs
  them. If the user has one, say so and offer to write the v3
  equivalent as a new descriptor (see "Migrating from v2").
- **`sbx kit validate` is not a conformance check.** The v0.50.1 code supplies
  a v3 builder to both normal `validate` and `inspect`. Both need an
  authenticated daemon; `--offline` deliberately omits the builder and
  rejects v3 source kits. A normal validate success is therefore allowed,
  but does not replace `kit-tck` or real runtime composition.
- Do not carry v2 vocabulary into v3: `name`, `sandbox:`,
  `permissions.network`, `credentials:`, `setup.*`, and `--kit-arg` are not v3
  fields, and v2 composition rules (additive allow lists, duplicate-service
  credential failures) are not established for v3.
- This skill is experimental. The source calls the schema-3 grammar
  unfinished and says the Go implementation wins over its docs, so re-check
  fine details against the spec before relying on them.
- No minimum `sbx` version for Kits v3 is established by the source, which
  says only that current stable releases support it in local and cloud mode.
  Check the installed `sbx` rather than assuming.

## When to use this skill

Activate this skill when:
- The user wants to create a new kit: package a CLI or agent as a kit, add a
  tool, credential, or policy to an existing agent, or add a `-mixin` variant.
- The user asks what a kit descriptor should contain, whether to write a
  workload or a mixin, or which capabilities a kit should request.
- The user wants to pin a tool version, declare `provides`/`requires`, or
  write the content recipe (`<kit>.dockerfile`) for a kit.
- The user wants to build, check, publish, or sign a kit, or to compose a
  built kit onto a workload and test it.
- The user has an existing v2 `spec.yaml` and wants it converted to v3.
- The user wants to reference, configure, or pin a kit from an `sbxenv.yaml`
  file's `agent:` and `kits:` fields, or asks which file fields a kit's
  capabilities need (bindings, mounts, ports).

## Do not use this skill when

Do not use this skill when:
- The task is creating, running, or removing the sandbox a kit is composed
  into, independent of the kit's own content — use
  `docker-sandboxes-lifecycle`.
- The task is what a credential or network rule actually does at runtime
  (proxy injection, allow/deny precedence, the policy a sandbox currently
  has), where a user stores a secret value, or secrets and policy unrelated
  to any kit — use `docker-sandboxes-network-credentials`.
- The task is the rest of an `sbxenv.yaml` file — lifecycle hooks, the
  approval plan, multi-file merging, user defaults, or the format of its
  `secrets:`/`registries:` blocks.
  No skill in this catalog owns those; use `docker-docs` to answer from the
  current Docker Docs environment files page. This skill owns only the
  `agent:`/`kits:` references and the fields a kit's capabilities map onto.
- The task is general Dockerfile or image-build optimization unrelated to a
  kit's recipe — use `docker-build-strategies`.
- The task is to author, validate, or debug a legacy v2 `spec.yaml`. It is out
  of scope; offer migration instead.
- The task is a bulk migration of v2 kits to v3. The source names a
  `migrate-kit-to-v3` skill and a field-by-field mapping, but that skill is
  not part of this catalog and may not be installed; do not route to it
  unless it is available. See "Migrating from v2" below.

## Core guidance

### v3: choose workload or mixin first

Everything else follows from the kind.

| | `kind: workload` | `kind: mixin` |
|---|---|---|
| Layers are | a root filesystem | an overlay landing on a workload |
| Per composition | exactly one | zero or more |
| Owns | entrypoint, env, user, workdir, a legacy context profile | env, labels, ports and volumes, which merge; an agent mixin can select an explicit context profile |
| Must have content | yes | no — may be declaration-only |

- Write a **workload** when you own the environment the agent runs in. Write a
  **mixin** when you add a tool, a credential, or a policy to somebody else's.
  Most new kits should be mixins; a tool worth shipping as a workload is
  usually worth shipping as both (the source's `claude` and `claude-mixin`
  examples are that pair).
- A mixin cannot set `ENTRYPOINT`, `CMD`, `USER` or `WORKDIR` and have it take
  effect: the workload anchors the composition and owns those fields. The
  additive fields merge (env, labels, ports, volumes), so a mixin's `ENV`
  reaches the composed image and `PATH` is appended rather than replaced.
- Prefer `ENV` for static environment: it is what the agent process sees,
  whereas profile and rc files do not run for the agent, so an
  `/etc/profile.d/<kit>-env.sh` drop reaches a terminal the user opens but not
  the agent. Use profile.d only when two mixins might set one variable to
  different values (a hard composition failure) or the value only makes sense
  in an interactive shell.

### v3: layout and descriptor

The default form is a companion pair found by filename stem: `<kit>/<kit>.yaml`
(first line `# syntax=docker/sandbox-kit:3`) and `<kit>/<kit>.dockerfile`
(omitted for a declaration-only mixin). Every key is `lowerCamelCase`, and
decoding is **strict**: an unrecognized key is an error, deliberately, because
a silently ignored misspelling would be a policy silently absent.

- `assets/v3-mixin-egress.yaml` is a complete declaration-only mixin. Its
  build and all 19 layout conformance checks passed on 2026-11-02; runtime
  composition initially failed on v0.50.1 because `agent-context@2` was
  required. The explanatory note is now optional; the network request remains
  required. Corrected composition and npm HTTPS access passed under the test
  host policy. See `checks/authenticated-results.md` for scope and limits.
- `references/v3-capabilities.md` has the annotated descriptor skeleton, the
  other authoring forms, and every capability type with its common mistakes.

### v3: capabilities — least privilege, and the rules most often missed

A capability is a typed request the host answers. The default is required and
fails resolution closed; `optional: true` means the kit degrades without it.
Request only what the kit needs. The rules below prevent the most common
failures; the full table is in `references/v3-capabilities.md`.

- `network-policy@1` is **phase-scoped**: an absent phase grants nothing.
  Install-hook hosts go in `install`, runtime hosts in `runtime`, shared hosts
  in both. `network-policy@2` bounds by HTTP method and path, is exclusive
  with `@1`, and its bound should be verified on the target runtime before it
  is treated as a security boundary.
- `credential@1` entries are required by default; add `optional: true` unless
  the kit cannot run unauthenticated. Every `inject[].domain` must appear
  exactly in each listed phase's allow list; a wildcard does not satisfy a
  specific subdomain. Never put secret values in a descriptor, arg, or recipe.
- `ssh-agent@1`: set `unrestricted: false` and bound it (`sign: [git]`,
  `authenticate: [git@github.com]`); the default signs anything with every key
  the user's agent holds. Prefer `credential@1` over HTTPS when a token will do.
- `lifecycle@1` hook environments are deny-by-default; declare every variable
  a hook or its child processes read, including `HTTP_PROXY`/`HTTPS_PROXY`.
- `privileged@1`, `host-mount@1`, `host-port@1` and `dockerd@1` widen what the
  kit can touch. Do not declare them on speculation; host mounts are shared
  with the host user and survive sandbox removal.
- Verify every flag in `agent-sessions@1` and `agent-interactive-sessions@1`
  against the tool's real CLI; never invent one.

### v3: versions, provides, and requires

- **Pin the tool once.** Declare a build-phase `version` arg, wire it through
  to the installer, and reference it from both `provides` and the top-level
  `version:`, so one value drives the install, the matchable capability, the
  published version, and the tag.
- **A pinned provide is a claim about content, so make the build enforce it:**
  re-read the installed version and fail on mismatch. Pinning the provide
  without pinning the install is worse than floating.
- **An unversioned provide is not a resting place.** Under `version: "1.0.0"`
  it publishes `<tool>@1.0.0`, the kit's release number wearing the tool's
  name; with no `version:` the build fails. Pin it, or drop the provide.
- **`requires` is a closed-set check.** A name nothing in the composition
  provides makes the kit refuse to compose anywhere. It constrains the
  composed runtime, not your build stage. Never require the platform floor
  (`bash`, `sh`, `curl`, `git`, a CA store, the `agent` user at uid 1000), and
  do not try to express a conditional dependency: let the hook probe and fail
  with an actionable message. The test is "what must already be present, on
  every base, for this kit to work at all"; usually that is nothing.
- Where a requirement is real, use `deb/` names (derived from a workload's
  dpkg database; on multi-platform workloads, the intersection across
  platforms), and never author a `deb/` provide yourself.

### v3: content recipes

Recipes for both kinds, the overlay ownership rules, the virtualenv trap, and
the audit are in `references/v3-recipes.md`. Read it before writing a mixin:
overlay ownership is the most common way a working-looking kit is broken. In
short: a mixin overlay stages under `/out` and copies into `scratch`, keeps
out of `/home/agent` where it can, and states numeric ownership for every
directory level it ships (`/home` root-owned, `/home/agent` uid 1000).

### v3: build, run, and verify

Create a named container builder once and select it for exports and
publication. The `docker` driver with the classic image store can drop
manifest annotations, leaving an image that is no longer a kit.

```sh
docker buildx create --name kit-builder --driver docker-container --bootstrap
```

```sh
# Run from the parent of <kit> and <workload>; subshells preserve that directory.
# 1. validate — the descriptor is checked before content is built. cacheonly
#    drops the EXPORT, not the build: once valid, the whole recipe still solves.
(cd <kit> && docker buildx build --builder kit-builder . \
  -f <kit>.yaml --output type=cacheonly)

# 2. build, exporting a layout so kit-tck can judge it without a registry
(cd <kit> && docker buildx build --builder kit-builder . -f <kit>.yaml -t <kit>:<version> \
  --output type=oci,dest=/tmp/<kit>-layout,tar=false)

# 3. conformance — the tag alone, not <kit>:<version>
kit-tck validate --layout /tmp/<kit>-layout <version>

# 4. run it, no registry needed
sbx run ./<kit> .                          # a workload
sbx run ./<workload> --kit ./<kit> .       # a mixin, composed
sbx kit inspect ./<kit>                    # requires authenticated daemon; see below
```

- `--app-name` isolates the Docker login store as well as daemon state.
  Sign in explicitly to the test app before normal source inspection.
  `--offline` is not an auth workaround for v3 sources: it deliberately
  disables the builder to keep the command daemon-free. The observed
  offline rejection is expected, not evidence that normal inspect is broken.
- v0.50.1 inspection shows a legacy-shaped summary, not the raw descriptor.
  Use `kit-tck inspect --descriptor --layout <layout> <tag>` to read the typed
  requests. Do not copy `sbx kit inspect --format json` output as v3 YAML.
- v0.50.1 supports v3 kits but not `agent-context@2` at composition time.
  Only mark this request optional when its guidance is nonessential, as in
  the egress asset; otherwise use a host with explicit support. Successful
  inspection/validation does not prove required capability availability.
- **A build is not proof the kit works.** For a mixin, compose the built
  overlay onto a real workload and run the tool with `sbx exec <sandbox> <tool>
  --version`. Arguments after `--` on `sbx run` are agent arguments, so they
  never execute the overlay's binary. Details and the ownership audit are in
  `references/v3-recipes.md`.
- Inside a sandbox the kit is self-describing: `/usr/share/sandbox/kit/<kit>/kit.yaml`
  is the published descriptor, `kit.dockerfile` the recipe, and
  `/var/log/sbx-kit-startup.log` the startup hook output.
- Local recipe builds use host Docker Buildx when available, otherwise the
  shared builder sandbox; see `references/v3-publish-and-sign.md` for the
  `BUILDX_BUILDER` and `SBX_KIT_BUILDER` selectors.
- Install `kit-tck` from a pinned release or commit, not `@latest`, and record
  which one you used. The source's `go install` line uses `@latest`.

### v3: publish and sign

Publishing is the build with `--push`: there is no pack step and no
`kit push` subcommand. Push both platforms in one invocation, tag the version
and `latest` together, and run `kit-tck validate` on the pushed reference.
Signing is optional: sign the digest from `--metadata-file`, never the tag,
and pin the whole certificate identity (repository, workflow file, and ref),
not an organization prefix. Commands and reasoning are in
`references/v3-publish-and-sign.md`.

A push writes to a registry and this skill cannot undo it. Get explicit
approval for the exact registry, repository, and tags first, and use a scratch
namespace for trials.

### v3: referencing a kit from sbxenv.yaml

An `sbxenv.yaml` (its own `schemaVersion: "1"`) composes kits through
`agent:` and `kits:`. The full rules and the capability-to-field table are in
`references/sbxenv-kit-references.md`; the ones that most affect kit authors:

- `agent:` is a built-in agent or the **handle** (last repository path
  segment, `dir=` basename, or directory name) of the single `kind: workload`
  kit under `kits:`; every other entry must be a mixin.
- An entry is a bare reference or `{source, args}`. Only `./…`, `../…`, `.`,
  `..`, or `*.zip` are local paths (resolved against the declaring file);
  pin OCI references as `tag@sha256:<digest>` and git ones with
  `#ref=<commit>`, because tags are republished.
- A published kit accepts only **create-phase** args; build-phase args such
  as `version` were fixed at publish time, so consumers change versions by
  changing the tag.
- A required `credential@1` without a `bindings:` entry makes create fail;
  an optional one is skipped silently. A `host-mount@1` path can be bound to
  a chosen host directory with an optional `mounts:` entry.
- `sbx env plan` does not resolve kit references, and a mixin that
  under-declares `requires` still plans cleanly. Only a disposable
  `sbx env create` proves a composition installs.

### Safety boundaries and inverse operations

- Never run source examples blindly. Build, run, push, and sign commands here
  are templates with placeholders; the operator runs them against disposable
  resources.
- **Inverse operations are destructive and need explicit confirmation:** the
  named builder is removed with `docker buildx rm kit-builder`, a test sandbox
  with `sbx rm` (flags in `docker-sandboxes-lifecycle`), and local test images
  with `docker rmi` (see `docker-destructive-guardrails`). Name only what you
  created. Removing a sandbox instance deletes its volumes; host-mounted data
  survives and stays visible to the host user.
- Keep descriptors, args, recipes, and build output free of secrets. Use
  `credential@1` for credentials and let the host answer it.
- A registry push, a tag move, and a signature are not reversible by this
  skill. State exactly what was pushed and signed.

### Migrating from v2

The v2-to-v3 field mapping is not part of the supplied source material, so this
skill does not map fields; do not guess one. For a request to convert a v2
`spec.yaml`: confirm the installed `sbx` can read v3, keep the v2 kit only as
a reference for intent, and write the v3 kit as a new descriptor using the
sections above. Check it with the v3 workflow (buildx, `kit-tck`, a real
composition); do not substitute `sbx kit validate` for those checks. If the
`migrate-kit-to-v3` skill or its mapping is available in the user's environment, use it as an
additional reference and say that it came from outside this catalog.

## Related skills

- For the sandboxes a kit is composed into (`sbx create`/`run --kit`, and
  removing a test sandbox), use `docker-sandboxes-lifecycle`.
- For what a kit's credential and network declarations mean at runtime (proxy
  injection, allow/deny precedence, the effective policy once global or
  per-sandbox policy is included, where the user stores a secret value), use
  `docker-sandboxes-network-credentials`. That skill's vocabulary is v2-era;
  for v3, the capability rules in this skill apply to what a kit asks for.
- For `sbxenv.yaml` fields beyond `agent:`, `kits:`, and the capability
  mappings above, no skill in this catalog applies; use `docker-docs` to answer
  from current Docker Docs.
- For Dockerfile and build practices beyond kit recipes, use
  `docker-build-strategies`.
- Before removing builders, images, or volumes created while testing a kit,
  use `docker-destructive-guardrails`.

## References

- `references/v3-capabilities.md` — v3 descriptor skeleton, authoring forms, every capability type with common mistakes, volume and host-mount semantics, groups, and final-environment references.
- `references/v3-recipes.md` — workload and mixin overlay recipes, ownership rules, and how to verify an overlay.
- `references/v3-publish-and-sign.md` — publishing with buildx, tagging, cosign signing and verification, and tooling notes.
- `references/sbxenv-kit-references.md` — `agent:`/`kits:` reference shapes, handles, kit args, pinning, the capability-to-`sbxenv.yaml` field mapping, and what `sbx env plan` does not prove.
- `references/sources.md` — provenance, unverified claims, and conflicts.

## Assets

- `assets/v3-mixin-egress.yaml` — a complete declaration-only v3 mixin
  (`schemaVersion: "3"`) with a required network-policy request and optional explanatory agent context.

## Checks

- `checks/verification.md` — a manually exercised v3 runbook (inspect, buildx descriptor check, `kit-tck`, strict decoding, daemon-backed validation versus offline rejection, optional composition, scoped cleanup). It uses isolated names and no registry publishing or signing.
- `checks/runtime-results.md` — 2026-11-02 commands, output, versions, pass/fail results, and the source-inspection limitation.
- `checks/authenticated-results.md` — authenticated A2/A6/A7, original failures, descriptor correction, successful runtime checks and cleanup.
- `scripts/audit-layer-owners.py` — fail-closed numeric ownership inventory of manifest-referenced OCI layers (Python 3.11+; uncompressed/gzip layers).
