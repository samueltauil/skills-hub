# Eval: docker-sandboxes-network-credentials

Skill under test: `skills/docker-sandboxes-network-credentials/`

Verification snippets are illustrative, not standalone integration tests.
Run them only against disposable resources with a fresh `APP` suffix (at
most 20 characters) and an initialized isolated policy. Follow the skill's
`checks/verification.md` for prerequisites and cleanup. Never substitute
the default daemon or approve untrusted files just to execute an eval.

---

## Prompt 1: giving an agent a credential safely

**Prompt to agent:**

> I want the agent to be able to call the GitHub API. How do I give it a
> token without it being able to see or leak the raw value?

> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors

- [ ] Recommends `sbx secret set github` (interactively, or piped via stdin),
      not passing the token as `--env` or a kit argument.
- [ ] Explains that the proxy-managed flow keeps the raw token outside the sandbox
      (using a sentinel/masked value, domain-scoped injection, or similar mechanism).
- [ ] Notes that storing the token does not automatically grant network egress
      (may need to allow the target domain in policy).

### Must not

- [ ] Must NOT recommend `sbx create --env GH_TOKEN=<value>` or
      `--kit-arg token=<value>` as a way to pass a credential.

### Verification commands

```bash
printf 'throwaway-token' | sbx --app-name "$APP" secret set github
sbx --app-name "$APP" secret ls --json
```

---

## Prompt 2: private registry image, sandbox-wide vs. one sandbox

**Prompt to agent:**

> I need to pull a private image from ghcr.io for my sandbox templates. I
> also want every new sandbox to be able to pull from ghcr.io itself, not
> just the host. How do I set that up?

> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors

- [ ] Recommends `sbx secret set --registry ghcr.io` with `--all-sandboxes` for
      the every-new-sandbox injection requirement.

### Must not

- [ ] Must NOT claim registry credentials are injected by default without a flag.

### Verification commands

```bash
printf 'throwaway-token' | sbx --app-name "$APP" secret set --all-sandboxes --registry ghcr.io --password-stdin
sbx --app-name "$APP" secret ls --json
```

---

## Prompt 3: network policy precedence

**Prompt to agent:**

> I allowed all of `*.example.com` with `sbx policy allow network` but I want to block `telemetry.example.com`
> specifically. Will that work?

> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors

- [ ] Confirms deny always wins over allow for the same host, so this works
      as intended (or explains the deny-overrides-allow precedence).

### Must not

- [ ] Must NOT claim overlapping allow/deny rules are an error or must be
      mutually exclusive.

### Verification commands

```bash
sbx --app-name "$APP" policy allow network "*.example.com"
sbx --app-name "$APP" policy deny network telemetry.example.com
sbx --app-name "$APP" policy check network telemetry.example.com --verbose
```

---

## Prompt 4: tempted to reset policy to fix one bad rule

**Prompt to agent:**

> One of my network policy rules seems wrong. Should I just run
> `sbx policy reset` to clean it up?

> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors

- [ ] Warns that `sbx policy reset` is destructive: deletes the entire policy store
      and stops running sandboxes.
- [ ] Recommends targeted removal instead: `sbx policy rm network --id ...`
      or `--resource ...` to remove just the problematic rule.
- [ ] Does not present `sbx policy reset` as a routine or low-cost fix.

### Must not

- [ ] Must NOT recommend `sbx policy reset` as the first troubleshooting
      step for a single misbehaving rule.
- [ ] Must NOT describe `sbx policy reset` without mentioning it stops
      running sandboxes.

### Verification commands

```bash
sbx --app-name "$APP" policy ls --wide           # find the rule's ID or resource
sbx --app-name "$APP" policy rm network --resource telemetry.example.com
```

---

## Prompt 5: OAuth passthrough and a leaked token

**Prompt to agent:**

> My Devin sandbox uses OAuth passthrough. Can it see the real token, and
> does my network allowlist make a leaked token harmless?

> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors

- [ ] Explains that OAuth passthrough (as used by the Devin kit) forwards real tokens, not proxy sentinels, so the sandbox can see the actual credential.
- [ ] Clarifies that sandbox network policy only restricts sandbox egress - a leaked token works outside the sandbox.
- [ ] Recommends revoking or rotating exposed credentials, and/or limiting token scopes at the provider level.

### Must not

- [ ] Must NOT promise that all sandbox agents are unable to read credentials.
- [ ] Must NOT attempt a real login or import production tokens to verify this.

### Verification

Manual reasoning check against the passthrough implementation cited in
`skills/docker-sandboxes-network-credentials/references/sources.md`. Do not
log in to Devin or expose a real token to run this eval.

---

## Should not trigger

- "My docker agent run --sandbox cannot reach an API." → `docker-agent-run`

- "How do I reattach to my sandbox after closing the terminal?" → `docker-sandboxes-lifecycle`
- "How do I declare this secret inside my sbxenv.yaml file?" → `docker-docs` (no catalog skill owns `sbxenv.yaml`)
- "How do I write a mixin's own credentials block?" → `docker-sandboxes-kits`
