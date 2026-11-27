# Sources

## v3 track: docker/sandbox-kit-spec at 4d932451613f8df89c8468e2bb7c5286882897ca

Adapted, not copied, from the operator-supplied authoring skill and recipes.
Their paths and content were confirmed through the GitHub contents API on
2026-11-02 at the pinned commit:

- [create-kit-v3/SKILL.md](https://github.com/docker/sandbox-kit-spec/blob/4d932451613f8df89c8468e2bb7c5286882897ca/skills/create-kit-v3/SKILL.md)
- [create-kit-v3/RECIPES.md](https://github.com/docker/sandbox-kit-spec/blob/4d932451613f8df89c8468e2bb7c5286882897ca/skills/create-kit-v3/RECIPES.md)

These sources establish authoring guidance, not support in every sbx release.
The source's blanket rejection claim about `sbx kit validate` is contradicted
by the recorded v0.50.1 tests and is corrected in this skill.

Where each part went:

- `create-kit-v3` `SKILL.md`: kind decision, layout, and the workflow in this
  skill's `SKILL.md`; the descriptor skeleton, capability table, volume and
  host-mount rules, bundled skills, groups, and environment references in
  `v3-capabilities.md`; publishing and signing in `v3-publish-and-sign.md`.
- `RECIPES.md`: `v3-recipes.md`, with its links to the source `SKILL.md`
  rewritten to this skill's `SKILL.md`.
- `assets/v3-mixin-egress.yaml` is original to this adaptation. It uses only
  descriptor keys and capability types that appear in the source skeleton,
  and it passed build and layout conformance checks on 2026-11-02. After
  making explanatory context optional, runtime composition and npm HTTPS
  connectivity also passed on v0.50.1; see the scoped evidence below.

Changes made while adapting (not source behavior):

- The workload recipe's `ENTRYPOINT` no longer carries a permission-bypass
  flag, and a checksum-pinning note was added.
- `kit-tck` installation is described as pinned rather than `@latest`.
- Approval, scratch-namespace, and inverse-operation (cleanup) guidance was
  added around registry pushes, builders, test sandboxes, and local images.
- References to source-repository paths (`examples/...`, the `migrate-kit-to-v3`
  skill and its `FIELD-MAPPING.md`) were removed or marked unavailable, since
  they are not part of this catalog and were not supplied.

## Public specification cross-check

Fetched and read these pinned public pages on 2026-11-02:

- [SPEC-v3](https://github.com/docker/sandbox-kit-spec/blob/4d932451613f8df89c8468e2bb7c5286882897ca/docs/spec/SPEC-v3.md): §3 companion-pair authoring;
  §7 typed requests, optionality and unknown types; §10 staged descriptors,
  additive image-config merging, PATH appending, overlay ownership and link
  checks; §12 the platform floor. These are specification contracts, not
  proof that every recipe base or runtime implements them.
- [network-policy@1](https://github.com/docker/sandbox-kit-spec/blob/4d932451613f8df89c8468e2bb7c5286882897ca/docs/spec/capabilities/com.docker.sandbox/network-policy@1.md)
  and [network-policy@2](https://github.com/docker/sandbox-kit-spec/blob/4d932451613f8df89c8468e2bb7c5286882897ca/docs/spec/capabilities/com.docker.sandbox/network-policy@2.md):
  phase-scoped policy, mutually exclusive versions within one descriptor,
  bounded request shapes, deny precedence and fail-closed runtime duties.
- [agent-context@2](https://github.com/docker/sandbox-kit-spec/blob/4d932451613f8df89c8468e2bb7c5286882897ca/docs/spec/capabilities/com.docker.sandbox/agent-context@2.md):
  inline content, profiles, selected-version exclusivity and runtime surfacing.
  The page explicitly requires consumers to advertise @2 support before
  accepting required requests; schema version 3 alone is insufficient.
- [dockerd@1](https://github.com/docker/sandbox-kit-spec/blob/4d932451613f8df89c8468e2bb7c5286882897ca/docs/spec/capabilities/com.docker.sandbox/dockerd@1.md):
  `autoStart`, privilege/storage surface and runtime refusal.
- [host-mount@1](https://github.com/docker/sandbox-kit-spec/blob/4d932451613f8df89c8468e2bb7c5286882897ca/docs/spec/capabilities/com.docker.sandbox/host-mount@1.md):
  runtime-owned host location, shared storage identity and persistence.

The pinned authoring skill also states that its grammar is unfinished and
implementation wins on disagreement. This verifies that attribution, not
that every implementation behavior conforms to the specification. The other
capability summaries remain source-derived guidance; consult the
[pinned capability directory](https://github.com/docker/sandbox-kit-spec/tree/4d932451613f8df89c8468e2bb7c5286882897ca/docs/spec/capabilities/com.docker.sandbox)
before using a type. Runtime support must still be checked on the target host.

## Removal of the legacy v2 track

An earlier revision of this skill also covered v2 `spec.yaml` kits
(`schemaVersion: "2"`, verified against docker/sandboxes
`df5c96ba60484fa2c375469dbac912c205da6c37`). That guidance, its assets, and
its evidence were removed on the operator's instruction that v2 is being
retired and v3 is the standard. That retirement is an operator statement; the
supplied v3 source gives no deprecation or removal timeline for v2, so this
skill gives no date and cites no source for it.

The earlier evidence is in the Git history of this repository, not in this
skill. Nothing in the v3 sources was used to restate, confirm, or extend it.

## Remaining scope limits and review questions

The tested example is not a certification of the whole skill:

1. `sbx v0.50.1` is a tested local release, not the first supporting release
   or evidence for cloud support. Do not infer capability support from the
   schema version; required `agent-context@2` failed on that release.
2. The capability table describes source/spec contracts. Only the egress
   example was exercised at runtime. Optional context delivery, bounded
   network security, credentials, privileged grants and other capabilities
   were not tested. A reviewer should check any broader claims against the
   pinned specification, not extrapolate from the HTTP 200 result.
3. PR image check run `41481808170` performed anonymous manifest/platform
   checks: 14 occurrences passed, one local CLI-output tag was misclassified,
   and `dhi.io/debian-base:trixie-dev` was not checked. The real references
   that passed were `docker/sandbox-kit:3`, `docker/dockerfile:1`, and the
   pinned `docker.io/sbx/shell-docker-image` index used by the runtime test.
   This establishes anonymous manifest availability with amd64/arm64 entries
   at check time, not full anonymous layer downloads or future tag stability.
   After correcting case-sensitive Compose-key detection, the full local
   `task images:check` passed: 66 occurrences, 21 unique references, 65 ok,
   zero errors/warnings, and the one unsupported-registry notice.
4. The illustrative `dhi.io` recipe bases and tool downloads are not verified.
   Inspect and pin a suitable base before using them; the platform floor is a
   spec requirement, not a verified property of every named image.
5. Tool-bearing overlays, env/file ownership interactions, volumes, host mounts,
   startup-log behavior, publishing and signing were not run. Source-backed
   recipes are templates that require their own build, TCK and runtime tests.
6. `BUILDX_BUILDER` and the in-sandbox descriptor path were exercised.
   `SBX_KIT_BUILDER` overrides were source-reviewed only.
7. No public v2 retirement policy was established. Excluding v2 is a routing
   decision for this skill, not a product deprecation/removal announcement.

## sbxenv.yaml kit references

`sbxenv-kit-references.md` carries over the kit-related rules from the
retired `docker-sandboxes-env` skill (removed from this catalog on
2026-11-12; last version 0.2.1 at commit
`188afba` of this repository). Its provenance was:

- [Docker Docs: Sandbox environment files](https://docs.docker.com/ai/sandboxes/configuration/environment-files/),
  retrieved 2026-11-10: `agent:`/`kits:` shapes, relative-source resolution,
  create-phase args, `kit.allowedSources`, `--kit-arg`/`--kit-args-file`,
  `mounts:`, `ports:`, `bindings:`, `registries:`, and the
  recreate-on-change rule.
- Installed `sbx env` help, sbx v0.51.0
  (`7d55286de0c775148b985ed349f760f1eba06203`): flag availability.
- docker/sandboxes `sandboxlib/sbxenv/types.go` and `sandboxlib/kit/git.go`
  at the same commit (internal, not publicly verifiable): the
  `git+…#ref=…&dir=…` source shape.
- [docker/sandbox-kit-spec `skills/sbxenv`](https://github.com/docker/sandbox-kit-spec/tree/75b2696a80163497b0d0d1cd73d3fb7ccaa050fe/skills/sbxenv)
  at `75b2696a80163497b0d0d1cd73d3fb7ccaa050fe`: handle rules and the
  capability-to-field handling.
- Runtime observations recorded by that skill on sbx v0.51.0, macOS arm64,
  2026-11-10 and 2026-11-12, and not re-run for this skill: `sbx env plan`
  accepted a nonexistent tag and a nonexistent kit; the nonexistent tag failed
  only at create; `sbx/playwright:1.61.1` (`requires: []`) failed at create on
  the `shell` agent with `env: 'node': No such file or directory`;
  `sbx/task:3.50.0` composed and ran; the `sbx/playwright` tag was republished
  with a new digest; and `shell` resolved as `docker.io/sbx/shell`.
- The local-workload `shell` name collision comes from this skill's own
  v0.50.1 runtime results, not from the environment-file sources. The
  `docker buildx imagetools inspect` pinning example and the upgrade
  checklist's descriptor-comparison step are this adaptation's
  substitutes for the retired helper and have not been exercised against an
  `sbxenv.yaml`.

`sbx env` and environment-file `schemaVersion: "1"` are experimental. The
retired skill's live Docker Hub helper (`scripts/kits.py`) was not carried
over; this skill does not search or rank the public kit catalog.

## Conflicts and gaps

- `docker-sandboxes-lifecycle` states that `sbx --cloud` is out of scope for
  its skill set, while the v3 source says Kits v3 work in cloud mode. This
  skill makes no cloud-mode claims of its own.
- The v2-to-v3 field mapping (`FIELD-MAPPING.md` in the source's
  `migrate-kit-to-v3` skill) was not supplied. No mapping is given here, and
  `migrate-kit-to-v3` is not a skill in this catalog.
- The kit-spec source does not say how v3 credential values are provided to
  a sandbox (for example whether `sbx secret set` applies), or how `args` are
  supplied at create time. The `sbxenv.yaml` and `--kit-arg` rules in
  `sbxenv-kit-references.md` come from the separate sources listed under
  "sbxenv.yaml kit references" above, not from the kit spec.
- The sibling skills `docker-sandboxes-lifecycle` and
  `docker-sandboxes-network-credentials` still describe kits in v2-era
  vocabulary (`spec.yaml`, `credentials:`, `permissions.network:`). Their
  routing to this skill remains correct, but their wording has not been
  reconciled with v3.
- The original adaptation was unexecuted. The 2026-11-02 verification below
  supersedes that statement for build/layout checks, authenticated source
  loading and the corrected asset's local runtime composition. Publishing and
  signing remain untested.

## Executed verification: 2026-11-02

See [commands and output](../checks/runtime-results.md). Tested on macOS arm64,
Docker Engine 29.9.1 / Desktop 4.96.0, Buildx v0.38.0, and `sbx v0.50.1`
(`ddb0268d7124b9cf98955d0b08ffd71a0dfcebe4`). `kit-tck` was installed at
`4d932451613f8df89c8468e2bb7c5286882897ca`; its version command printed `dev`,
while Go build metadata recorded
`v3.0.0-m.11.0.20261031103226-4d932451613f` (Go 1.26.10).

Verified, scoped to this asset and these tools:

- A3: declaration-only companion-pair descriptor builds with `cacheonly`.
- A4: OCI directory export and bare-tag `validate --layout ... 0.0.0`
  succeed: **19 checks, 19 passed**. No correction was needed for build
  conformance; runtime testing later required making explanatory context optional.
- A5: misspelling `capabilities` as `capabilites` fails strict decoding and
  names the bad field.
- A6: the offline source validation path rejects this v3 source kit with
  "no kit builder configured; artifact validation failed". The normal
  command's sign-in failure alone is not evidence for v3 rejection.
- The frontend pulled as `docker/sandbox-kit:3` at
  `sha256:adbc0d1ea63451871d5d78111120bb29f2fd2b265e63d39c664ae2c3d722c805`,
  reporting `3.0.0-m.11 (92835bb7)`.

Initial-run limit: normal inspection stopped at sign-in, and offline
inspection rejected the source as expected for a builder-free path. A7 was
skipped without a trusted workload. That initial run did not verify runtime
behavior; see the authenticated follow-up below for subsequent evidence.
A1/A8 created and removed only that run's builder and scratch resources.

## Source follow-up: A2 and A6

Inspected the operator's `docker/sandboxes` checkout at
`aaa96b72111a83a8326419630ab6ad18c0fde0c5` and used `git show` to read the exact
installed v0.50.1 revision `ddb0268d7124b9cf98955d0b08ffd71a0dfcebe4`.
These code findings explain the initial failures; authenticated results
are recorded in the follow-up below:

- `cli-plugin/commands/kit.go`: normal validate sets
  `V3Builder: defaultKitBuilder{}`; offline validate/inspect deliberately omit
  it. `images_mirror.go` supplies that builder for normal inspect.
- `sandboxlib/kit/source_v3.go`: the observed error is the nil-builder guard,
  before descriptor build. `TestKitInspectCmd_OfflineRejectsV3SourceKit` and
  `TestKitValidateCmd_OfflineRejectsV3SourceKit` explicitly expect it.
- This design was introduced by commit
  `865f481537d6bb6d3951e5a2ff4cf70fcb748343` (2026-10-08), present in the
  installed release. No CLI patch or upgrade is needed to explain A2.
- `sandboxlib/auth/defaultstore.go`: a non-default app name selects a separate
  auth store, so the default app's login is not inherited.
- The original blanket claim "validate does not accept v3 source" is wrong:
  normal validation is builder-enabled in v0.50.1. A6's offline failure
  cannot support that claim. Authenticated validation subsequently passed.
- v0.50.1 `kit_source_builder.go` selects host Buildx or the sandbox builder;
  the current checkout adds in-process synthesis for declaration-only kits,
  followed by daemon import. Do not conflate these implementations.
- Installed help spells detached mode `--detach`, not the original A7
  `--detached`; the runbook now uses the supported spelling.

A7 candidate: the checkout's `tests/e2e/kits/testdata/shell` is a two-file v3
workload with `ENTRYPOINT ["sh"]` and only `com.docker.sandbox/sbx@1`.
For a disposable copy, pin its base `docker.io/sbx/shell-docker-image` to the
resolved index digest
`sha256:6c84996b07b743154fc8f26c662b642cee8fb6dd410803b2c40d5d3a537c838d`.
The index includes linux/arm64. The disposable workload was renamed to
`kit-probe` because v0.50.1 rejects a kit named `shell` as a collision with its
built-in agent. The operator signed in only to the isolated app; no auth
bypass or credential copying was attempted.

## Authenticated runtime follow-up: 2026-11-02

[Full commands and output](../checks/authenticated-results.md) supersede the
initial run's A2/A6/A7 conclusions. The same sbx v0.50.1 binary was used after
operator sign-in to an isolated app; no Sandboxes code change was needed.

- A2 succeeds but prints a projected summary, not both typed capabilities.
  Its JSON uses `newKitV2View`; do not copy that output into a v3 descriptor.
- A6 normal validate succeeds (`valid (directory)`); offline fails intentionally.
  Thus the original "must fail" expectation was wrong.
- A7 initially rejects required `agent-context@2` despite successful validation.
  The host does not support it. Corrected the asset to make only the
  explanatory context optional, leaving the network request required.
- The fixture stem `shell` also collides with a v0.50.1 built-in agent;
  renaming the disposable companion pair to `kit-probe` resolves this.
- Corrected A3/A4/A5 pass again: 19 TCK checks, raw descriptor inspection,
  and explicit rejection of `capabilites`.
- Corrected A7 starts the composed sandbox, policy check allows npm:443,
  and an in-sandbox curl returns HTTP 200. The kit descriptor is present at
  `/usr/share/sandbox/kit/extra-egress/kit.yaml`; exec runs as uid 1000.
- This tests the observed host policy, not whether the mixin alone added
  access: the host also permits package registries. Optional context delivery
  is not verified; neither are cloud, signing or other capabilities.
- All run-created sandboxes, builders, scratch directories and isolated daemon
  runtime state were removed. The operator's isolated sign-in was preserved.
