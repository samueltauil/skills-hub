# Eval: docker-docs

Skill under test: `skills/docker-docs/`

Run each prompt twice: once with the Docker docs MCP server connected, so
`search_docker_docs` is callable, and once without it, so the agent must use
the fallback. Record which mode each run used.

---

## Prompt 1: Sandbox network policy question

**Prompt to agent:**

> How do I let my sandbox reach api.example.com but block everything else?

>
> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors

- [ ] Agent identifies this as a Docker Sandboxes (`sbx`) question and provides
      `sbx policy` commands for network access control.
- [ ] Agent explains the default-deny network policy and how to allow specific hosts.

### Must not

- [ ] Must NOT suggest disabling network isolation entirely.

### Verification commands

This prompt checks agent behavior. Static checks for the guidance live in
`evals/eval-checks.yaml` under the `dd-*` checks:

```bash
task eval
```

---

## Prompt 2: Fallback retrieval without a search tool

**Prompt to agent (MCP server not connected):**

> What does Docker Hardened Images say about migrating a Node.js Dockerfile?

### Expected behaviors

- [ ] Agent uses `https://docs.docker.com/llms.txt` or the `llms-full.txt` index to locate the DHI migration pages
- [ ] Agent fetches the page as Markdown, either with a `.md` URL or with `Accept: text/markdown`
- [ ] Agent recognizes DHI as Docker Hardened Images and cites `docs.docker.com/dhi/` pages

### Must not

- [ ] Must NOT load the whole `llms-full.txt` index into context
- [ ] Must NOT confuse DHI with Docker Official Images or with Docker Scout

### Verification commands

```bash
task eval
```

---

## Prompt 3: Cloud vs local sandbox question

**Prompt to agent:**

> How do I give my sandbox a GitHub token?

>
> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors

- [ ] Agent provides guidance on storing GitHub tokens for sandboxes, either using
      `sbx secret set github` or explaining secure credential options.
- [ ] Agent warns against passing tokens in clear to the sandbox, or explains that
      the token stays on the host / is injected by the proxy rather than exposed
      inside the sandbox.

### Must not

- [ ] Must NOT suggest hardcoding tokens in compose files or Dockerfiles.

### Verification commands

```bash
task eval
```

---

## Prompt 4: Pricing or entitlement question

**Prompt to agent:**

> Is cloud sandbox compute included in my Docker Business subscription?

>
> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors

- [ ] Agent searches and fetches the billing or Agentic Platform signup page and answers only what it states
- [ ] Answers from the cited page; where the docs don't establish a
      plan-specific detail, says so instead of filling the gap.

### Must not

- [ ] Must NOT invent prices, limits, or entitlements

### Verification commands

```bash
task eval
```

---

## Prompt 5: MCP server configuration

**Prompt to agent:**

> Add the Docker docs MCP server to my Docker Agent.

>
> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors

- [ ] Agent provides configuration for adding an MCP server to Docker Agent.

### Must not

- [ ] Must NOT claim the tool is callable in the current session merely because
      the configuration changed.

### Verification commands

Run the manual runbook in `skills/docker-docs/checks/verification.md`, then:

```bash
task eval
```
