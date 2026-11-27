# Sources

- `docker agent --help`, `docker agent new --help`, `docker agent setup --help`, `docker agent debug --help`, `docker agent debug config --help`, `docker agent debug toolsets --help`, `docker agent models --help` — verified locally against docker-agent as shipped with Docker CLI 29.7.2.
- https://docs.docker.com/ai/docker-agent/concepts/agents/ — agent properties table, root agent, model fallbacks, named commands.
- https://docs.docker.com/ai/docker-agent/configuration/agents/ — full agent config schema (skills, hooks, compaction, redact_secrets, prompt files).
- https://docs.docker.com/ai/docker-agent/configuration/overview/ — variable expansion in prompt/text fields, including `${env.VAR}`; `token_key` takes an environment variable name rather than an expanded value.
- https://docs.docker.com/ai/docker-agent/guides/secrets/ — authentication credential handling and pattern-based redaction as defense in depth, not a guarantee against all secret leaks.
- https://docs.docker.com/ai/docker-agent/providers/overview/ — supported providers, quick comparison table, additional built-in provider aliases and their env vars.
- https://docs.docker.com/ai/docker-agent/providers/custom/ — `providers:` section, provider properties, shorthand syntax, global providers in `~/.config/cagent/config.yaml`.
- https://github.com/docker/docker-agent/blob/main/docs/index.md — top-level concepts, "why Docker Agent", MCP catalog and Docker Model Runner composition, glossary (Agent, Tool, MCP, A2A, TUI, OCI).
- https://docs.docker.com/ai/docker-agent/ — product overview, install paths (Docker Desktop 4.63+, Homebrew, winget, GitHub releases), example agent.yaml.
- https://docs.docker.com/ai/docker-agent/community/troubleshooting/ — "No model is currently available" / "model ... is not pulled" pitfalls and `docker agent doctor` usage.
