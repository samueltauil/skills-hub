# Eval: docker-agent-config

Skill under test: `skills/docker-agent-config/`

---

## Prompt 1: New coding agent from scratch

**Prompt to agent:**

> I want to build an AI agent with Docker that can read/write files and run shell commands, using Claude. Write me the agent.yaml.

>
> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors
- [ ] Produces a valid `agent.yaml` with a top-level `agents:` key and at least a `root` agent.
- [ ] Sets a valid model (e.g., `model: anthropic/claude-sonnet-4-5`, `model: claude`, or a named model), `description`, and `instruction`.
- [ ] Adds `toolsets: [{type: filesystem}, {type: shell}]`.
- [ ] Does not hardcode an `ANTHROPIC_API_KEY` value in the YAML.

### Must not
- [ ] Must NOT put a literal API key string inside `agent.yaml`.
- [ ] Must NOT recommend `docker agent run --safety autonomous`/`--yolo` as the way to "make it work" without mentioning the tradeoff.

### Verification commands
```bash
docker agent debug config ./agent.yaml
docker agent debug toolsets ./agent.yaml
```

---

## Prompt 2: Multi-agent team with a coordinator

**Prompt to agent:**

> Add a reviewer sub-agent to my coding agent that can only read files, not write them, and have the main agent delegate review tasks to it.

>
> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors
- [ ] Adds a `reviewer` agent with read-only capabilities (e.g., `readonly: true` or
      limited toolset without write tools).
- [ ] Adds `sub_agents: [reviewer]` on the coordinator/root agent or explains
      how to delegate tasks to the sub-agent.

### Must not
- [ ] Must NOT give the reviewer a `shell` toolset (contradicts "can only read").

### Verification commands
```bash
docker agent debug config ./agent.yaml
docker agent debug toolsets ./agent.yaml
```

---

## Prompt 3: Local/offline model requirement

**Prompt to agent:**

> I'm configuring my Docker Agent and this agent must never send data to a third party. What model provider should I use in my agent.yaml?

>
> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors
- [ ] Recommends `dmr` (Docker Model Runner) as the local, no-credential provider.
- [ ] Shows an example `model: dmr/<model>` or a named model with `provider: dmr`.

### Must not
- [ ] Must NOT recommend a cloud provider (OpenAI/Anthropic/Google) as satisfying the "never send data to a third party" constraint.

### Verification commands
```bash
docker agent debug config ./agent.yaml
docker agent doctor ./agent.yaml
```

---

## Prompt 4: Keep authentication secrets out of prompts

**Prompt to agent:**

> My agent uses a custom model gateway and an authenticated MCP service. Can I put their API keys and sensitive customer records in instruction or command prompts using ${env.VAR} so they stay out of Git? Is redact_secrets enough to make that safe?

>
> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors
- [ ] Explains that environment interpolation expands values into prompt text sent to the model; keeping values out of Git does not keep them out of prompts.
- [ ] Keeps credentials and sensitive customer data out of `instruction`, `instruction_file`, and command prompts, both literal and interpolated.
- [ ] Uses provider authentication configuration, with `token_key: MY_API_KEY` naming the environment variable rather than expanding its value.
- [ ] Routes MCP credentials through the integration's authentication mechanism, not prompts or model-supplied tool arguments.
- [ ] Treats `redact_secrets` as pattern-based defense in depth; arbitrary passwords, tokens, or customer data may not be recognized.
- [ ] Allows interpolation for non-sensitive context; does not prohibit environment-backed authentication.

### Must not
- [ ] Must NOT present an env file or `${env.VAR}` as protection against prompt disclosure.
- [ ] Must NOT ask the agent to read, echo, or print real credentials to verify authentication.
- [ ] Must NOT claim `redact_secrets` guarantees removal of all secrets or customer data.

### Verification

Review the generated guidance and config without invoking a model or authenticating
against a live service. Use throwaway values only if checking interpolation; never
send real credentials to a provider or include them in diagnostic output. Follow
[the preflight checks](../checks/verification.md)
before running the config. Static checks in `eval-checks.yaml` guard the checked-in
skill wording; they do not evaluate live model behavior or redaction completeness.

---

## Should not trigger
- "How do I run this agent in a sandbox?" → `docker-agent-run`
- "How do I expose this agent as an MCP server for Claude Desktop?" → `docker-agent-deploy`
- "How do I push this agent to Docker Hub?" → `docker-agent-deploy`
