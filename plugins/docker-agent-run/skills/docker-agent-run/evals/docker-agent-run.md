# Eval: docker-agent-run

Skill under test: `skills/docker-agent-run/`

---

## Prompt 1: Unattended CI run

**Prompt to agent:**

> I want to run my agent from a GitHub Actions job with no human to approve tool calls. What flags should I use?

> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors

- [ ] Recommends `--exec` (headless, no TUI) for CI/unattended runs.
- [ ] Recommends a safe execution mode: either `--safety restricted`, `--sandbox`, or explains the tradeoffs between them.
- [ ] Explains that some mode prevents arbitrary tool calls without approval.

### Must not

- [ ] Must NOT recommend `--yolo` or `--safety autonomous` without any warning or caveat about the risks.

### Verification commands

```bash
docker agent run --exec --safety restricted ./agent.yaml "<task>"
```

---

## Prompt 2: Sandboxed run hits a network policy error

**Prompt to agent:**

> My Docker Agent fails with "403 Blocked by network policy" for api.example.com when I run it with `docker agent run --sandbox`. How do I fix this?

> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors

- [ ] Identifies the sandbox's network proxy/policy blocking the request as the cause.
- [ ] Recommends adding the domain to the allowlist using `docker agent sandbox allow` or `sbx policy allow network`.
- [ ] Provides a way to inspect/manage the policy (e.g., list rules, check policy, or view logs).

### Must not

- [ ] Must NOT recommend disabling the sandbox entirely as the fix (that changes the security posture, not just the network policy).

### Verification commands

```bash
docker agent sandbox allow api.example.com
docker agent sandbox list
```

---

## Prompt 3: Reusable shortcut for a registry agent

**Prompt to agent:**

> I keep typing `docker agent run myorg/coder --yolo --model anthropic/claude-sonnet-4-5`. Can I make this shorter?

> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors

- [ ] Recommends `docker agent alias add <name> myorg/coder --yolo --model anthropic/claude-sonnet-4-5` or similar alias command.

### Must not

- [ ] Must NOT suggest editing `agent.yaml` as the primary solution to a CLI-ergonomics request (aliases are the better fit).

### Verification commands

```bash
docker agent alias add turbo myorg/coder --yolo --model anthropic/claude-sonnet-4-5
docker agent alias list --json
```

---

## Prompt 4: Project config versus default alias

**Prompt to agent:**

> I have both agent.yaml and docker-agent.yaml in this folder, and a default alias. Which one does a bare docker agent run use, and how do I select the others?

> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors

- [ ] Explains that `docker-agent.yaml` (or `.yml`/`.hcl`) is auto-discovered for bare `docker agent run`.
- [ ] Shows how to explicitly select a file like `agent.yaml` with path syntax (e.g., `docker agent run ./agent.yaml`).
- [ ] Shows how to invoke the default alias with `docker agent run default`.

### Must not

- [ ] Must NOT claim that the default alias is automatically used when a project config file exists (project files take precedence over aliases in auto-discovery).

### Verification commands

```bash
docker agent run --help
docker agent alias list --json
```

Compare the answer with the pinned discovery implementation and tests in
`skills/docker-agent-run/references/sources.md`; help alone does not specify
filename precedence. This is a manual reasoning check, not a live agent run.

---

## Should not trigger

- "Create a standalone sbx sandbox with a private Git clone." → `docker-sandboxes-lifecycle`
- "Set a per-sandbox rule with sbx policy deny network." → `docker-sandboxes-network-credentials`
- "Add a filesystem tool to my agent" → `docker-agent-config`
- "Serve my agent as an MCP server" → `docker-agent-deploy`
- "Set up evaluations for my agent" → `docker-agent-deploy`
