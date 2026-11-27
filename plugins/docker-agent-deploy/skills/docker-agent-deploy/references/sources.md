# Sources

- `docker agent serve --help`, `docker agent serve mcp --help`, `docker agent serve api --help`, `docker agent serve chat --help`, `docker agent serve a2a --help`, `docker agent serve acp --help`, `docker agent share --help`, `docker agent share push --help`, `docker agent share pull --help`, `docker agent eval --help` — verified locally against docker-agent as shipped with Docker CLI 29.7.2.
- https://docs.docker.com/ai/docker-agent/features/cli/ — full serve mode flag tables (default listen addresses, `--safety` default `restricted`, `--auth-token`/`--api-key`, `--session-workingdir-root`), and `share push`/`share pull` reference including signing (`--key`, `--encrypt`).
- https://docs.docker.com/ai/docker-agent/features/mcp-mode/ — MCP server mode setup and stdio vs `--http` transport.
- https://docs.docker.com/ai/docker-agent/features/evaluation/ — eval directory structure, eval session JSON schema, scoring metrics (Tool Calls F1, Relevance, Size, Assertions), `--baseline`/`--regression-tolerance` gate rules, provider-credential forwarding into eval containers.
- https://docs.docker.com/ai/docker-agent/concepts/distribution/ — agent distribution over OCI registries, `instruction_file` inlining on push, signing/encrypting agents.

> **Version note:** the docs above describe optional `--key`/`--encrypt` signing flags for `share push`/`share pull`. The locally installed `docker agent share push --help` / `docker agent share pull --help` (Docker CLI 29.7.2) show no such flags — do not tell a user to pass `--key`/`--encrypt` against this version; verify with `docker agent share push --help` before relying on signing.
