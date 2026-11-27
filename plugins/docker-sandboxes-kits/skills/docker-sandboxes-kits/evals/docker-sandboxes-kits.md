# Eval: docker-sandboxes-kits

Skill under test: `skills/docker-sandboxes-kits/`

The skill covers v3 kit descriptors only. Legacy v2 `spec.yaml` kits are out
of scope; a correct answer never presents a v2 command (`sbx kit validate`)
as validating a v3 descriptor.

Verification snippets are illustrative, not standalone integration tests.
Run them only against disposable resources with a fresh `APP` suffix (at
most 20 characters) and a uniquely named builder. Follow the skill's
`checks/verification.md` for prerequisites and cleanup. Never substitute the
default daemon, use a shared builder or registry, or approve untrusted files
just to execute an eval. The deterministic checks in `evals/eval-checks.yaml`
assert skill text and checked-in assets only, not live model behavior or a
live `sbx`.

---

## Prompt 1: a new kit for a CLI (mixin vs workload, version pin)

**Prompt to agent:**

> I want to package the `gh` CLI as a reusable Docker Sandboxes kit I can
> attach to any agent. How should I structure it, how do I pin the
> version, and how do I declare network access for both build-time downloads
> and runtime API calls?

>
> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors
- [ ] Recommends a v3 `kind: mixin` (it adds a tool to somebody else's
      environment) and explains the workload-versus-mixin distinction.
- [ ] Uses the companion-pair layout: `<kit>.yaml` whose first line is
      `# syntax=docker/sandbox-kit:3`, plus a `<kit>.dockerfile` content
      recipe.
- [ ] Declares one build-phase `version` arg that drives the install.
- [ ] Requests egress with phase-scoped `network-policy@1` (install versus
      runtime hosts).

### Must not
- [ ] Must NOT author a `spec.yaml`, use `schemaVersion: "2"` or
      `kind: sandbox`, or give `sbx kit validate` as the workflow.
- [ ] Must NOT add `requires: ["deb/curl"]` or similar for tools every base
      is entitled to provide.
- [ ] Must NOT present an unverified download URL or checksum as verified.

### Verification
Static: `assets/v3-mixin-egress.yaml` is the checked-in v3 example. For a
live check, follow `checks/verification.md` (builder, `kit-tck`,
`sbx kit inspect`) against a disposable builder.

---

## Prompt 2: mixin ownership of entrypoint and the agent's home

**Prompt to agent:**

> My mixin's Dockerfile sets `ENTRYPOINT` and `USER`, and it copies files with
> `COPY --chown=1000:1000 tool /home/agent/tool`. A reviewer says both are
> wrong. Why, and what should I do instead?

>
> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors
- [ ] Explains that a mixin cannot set `ENTRYPOINT`, `CMD`, `USER` or
      `WORKDIR` and have it take effect: the workload anchors the composition
      and owns them, while additive fields merge.
- [ ] Recommends staging under `/out` and using numeric ids for ownership,
      or avoiding `/home/agent` and using `/usr/local` or `/opt`.

### Must not
- [ ] Must NOT recommend using user names in chown (a `scratch` overlay has no
      `/etc/passwd`).

### Verification
Static text check against `references/v3-recipes.md`. Live: build the
overlay, export an OCI layout, and run `kit-tck validate --layout`.

---

## Prompt 3: is `sbx kit validate` enough for a v3 kit?

**Prompt to agent:**

> I wrote `my-kit.yaml` with `# syntax=docker/sandbox-kit:3`. Is
> `sbx kit validate ./my-kit` enough to know the kit is valid?

>
> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors
- [ ] Says no: normal `sbx kit validate` is not a substitute for conformance
      and runtime checks.
- [ ] Recommends additional validation steps beyond `sbx kit validate`, such as
      building the kit, running `kit-tck` conformance checks, or composition testing.
- [ ] Says a successful build is not proof the kit works.

### Must not
- [ ] Must NOT report `sbx kit validate` output as full kit conformance.

### Verification
Steps A2-A6 of `checks/verification.md`, including the check that
normal `sbx kit validate` can accept the source while `--offline` rejects it.

---

## Prompt 4: capabilities for network, a token, and hook environment

**Prompt to agent:**

> My v3 kit's install hook and the running agent both call `api.example.com`,
> and the API needs a token. Which capabilities should I declare, and what
> will go wrong if I get them slightly off?

>
> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors
- [ ] Uses `network-policy@1` and puts the host in both `install` and
      `runtime`, explaining that an absent phase grants nothing.
- [ ] Uses `credential@1` and discusses when to mark it `optional: true` (for
      APIs that work without auth) versus required (when auth is essential).
- [ ] Keeps the token out of the descriptor, args, and recipe.

### Must not
- [ ] Must NOT claim a wildcard entry satisfies a specific credential domain.
- [ ] Must NOT put a token value in a descriptor or build arg.

### Verification
Static text check against `references/v3-capabilities.md` and the skill's
core guidance.

---

## Prompt 5: publishing and signing a multi-platform v3 kit

**Prompt to agent:**

> How do I publish my v3 kit for amd64 and arm64 to our registry and sign it
> so consumers can verify where it came from?

>
> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors
- [ ] Explains that v3 kits are published via `docker buildx build --push` or similar
      build-and-push workflow (not `sbx kit push`).
- [ ] Mentions signing the image digest (not the tag) for verification.

### Must not
- [ ] Must NOT use `sbx kit push` or `sbx kit sign` for a v3 kit (these are v2 commands).
- [ ] Must NOT push two single-platform builds to the same tag (should use multi-platform build).

### Verification
Static text check against `references/v3-publish-and-sign.md`. Do not run a
real push in an eval.

---

## Prompt 6: an existing v2 kit and the migration skill

**Prompt to agent:**

> I have a kit with `schemaVersion: "2"` in a `spec.yaml`. Can you fix its
> validation error, and which skill converts it to v3 for me?

>
> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors
- [ ] Says legacy v2 `spec.yaml` kits are out of scope for this skill or
      explains that v3 uses a different format.
- [ ] Offers guidance on v3 kits or mentions where to get migration help.

### Must not
- [ ] Must NOT perform or claim to perform a mechanical field-by-field v2-to-v3 conversion
      (mentioning that a separate migration skill exists is acceptable).
- [ ] Must NOT treat `sbx kit validate` alone as conformance proof for a v3 kit
      (kit-tck is different and acceptable).

### Verification
Static text check against the skill's "Migrating from v2" guidance and
`references/sources.md`.

---

## Prompt 7: proving an overlay works when composed

**Prompt to agent:**

> My mixin builds and `kit-tck` passes, but I want proof the tool actually
> runs once it is composed onto a workload. What should I run?

>
> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors
- [ ] Composes the built overlay onto a real workload with
      `sbx run ./<workload> --kit ./<kit>` and runs the tool with
      `sbx exec <sandbox> <tool> --version`.
- [ ] Explains that arguments after `--` on `sbx run` are agent arguments and
      never execute the overlay's binary.

### Must not
- [ ] Must NOT suggest `sbx run ... -- tool --version` as the check.

### Verification
Static text check against `references/v3-recipes.md`. Live composition needs
an operator-supplied v3 workload (step A7 of `checks/verification.md`).

---

## Prompt 8: referencing a published kit from sbxenv.yaml

**Prompt to agent:**

> I published my `gh` mixin as `acme/gh:2.1.0`. How does a teammate add it to
> their checked-in `sbxenv.yaml` on top of the `claude` agent, and can they
> set the `gh` version there? The mixin requires a GitHub token.

>
> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors
- [ ] Keeps `agent: claude` and lists the mixin under `kits:`.
- [ ] Says the version of a published kit is chosen by its tag, not by a kit
      arg, because build-phase args were fixed at publish time.
- [ ] Approves the token through a `bindings:` entry (or the sbx credential
      store) rather than writing its value into the file.
- [ ] Recommends pinning a digest or says a clean `sbx env plan` does not
      prove the kit reference resolves.

### Must not
- [ ] Must NOT write a token value into `sbxenv.yaml` or a `--kit-arg`.
- [ ] Must NOT set `version` as a kit arg on the published kit.

### Verification
Static text check against `references/sbxenv-kit-references.md`. A live check
needs an operator-approved disposable `sbx env create` and `sbx env rm`.

---

## Should not trigger

- "How do I run this kit in a sandbox right now?" → `docker-sandboxes-lifecycle`
- "How do I actually store the API key value this credential needs?" → `docker-sandboxes-network-credentials`
- "How do I add a `postCreate` lifecycle hook to my sbxenv.yaml?" → `docker-docs` (no catalog skill owns the rest of `sbxenv.yaml`)
- "How do I shrink the layers of my application's Dockerfile?" → `docker-build-strategies`
- "Clean up the builders and images I created while testing" → `docker-destructive-guardrails`
