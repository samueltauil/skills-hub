# Toolsets and providers reference

## Built-in toolsets
Add by `type:` under an agent's `toolsets:` list — no external dependency required.

| type | Gives the agent |
| --- | --- |
| `filesystem` | Read, write, list, search, navigate files and directories |
| `shell` | Execute shell commands synchronously |
| `background-jobs` | Run and manage long-running shell commands |
| `think` | Step-by-step reasoning scratchpad for planning/decision-making |
| `todo` | Task list management for multi-step workflows |
| `tasks` | Persistent task database shared across sessions |
| `memory` | Persistent key-value storage backed by SQLite (`save_memory`, `search_memories`) |
| `fetch` | Read content from HTTP/HTTPS URLs (GET only) |
| `script` | Define custom shell scripts as named tools |
| `lsp` | Connect to Language Server Protocol servers for code intelligence |
| `api` | Create custom tools that call HTTP APIs without writing code |

Source: https://docs.docker.com/ai/docker-agent/configuration/tools/ (linked from https://docs.docker.com/ai/docker-agent/concepts/tools/).

## MCP toolsets — three connection modes
1. **Docker MCP (recommended)** — runs the MCP server in a container via the
   MCP Gateway; browse servers at https://hub.docker.com/search?q=&type=mcp.
   ```yaml
   toolsets:
     - type: mcp
       ref: docker:duckduckgo
   ```
2. **Local MCP (stdio)** — runs an MCP server as a local process over
   stdin/stdout.
3. **Remote MCP (Streamable HTTP / SSE)** — connects to an MCP server over
   the network; see Remote MCP Servers docs for OAuth details.

Add `defer: true` to any MCP toolset entry to load its tools lazily instead
of at agent startup.

Source: https://docs.docker.com/ai/docker-agent/concepts/tools/ (MCP Tools section).

## Providers and required credentials

| Provider key | Local? | Credential |
| --- | --- | --- |
| `openai` | No | `OPENAI_API_KEY` |
| `anthropic` | No | `ANTHROPIC_API_KEY` |
| `google` | No | `GOOGLE_API_KEY` |
| `amazon-bedrock` | No | AWS credentials |
| `dmr` (Docker Model Runner) | Yes | None — model must be pulled with `docker model pull` |
| `ollama` | Yes | None (optional `base_url`) |
| `mistral` | No | `MISTRAL_API_KEY` |
| `groq` | No | `GROQ_API_KEY` |
| `xai` | No | `XAI_API_KEY` |
| `together` | No | `TOGETHER_API_KEY` |
| `deepseek` | No | `DEEPSEEK_API_KEY` |
| `azure` | No | `AZURE_API_KEY` + `base_url` |
| `github-copilot` | No | `GITHUB_TOKEN` (PAT with `copilot` scope) |
| `chatgpt` | No | None — sign in via `docker agent setup` |
| custom OpenAI-compatible | depends | `token_key` env var + `base_url` you define under `providers:` |

This is not exhaustive — credential requirements can vary by alias and by
version; run `docker agent models --all` for the authoritative,
installed-version list. Source: https://docs.docker.com/ai/docker-agent/providers/overview/.

## Named models vs inline models
- Inline: `model: openai/gpt-5` directly on the agent — quick, no reuse.
- Named: define under top-level `models:`, referencing a `provider:` and
  `model:`, then set `temperature`, `max_tokens`, `thinking_budget`, etc.
  Reference it by name from any agent. Prefer named models once more than
  one parameter needs tuning or more than one agent shares the model.

Source: https://docs.docker.com/ai/docker-agent/concepts/models/ (linked from
https://docs.docker.com/ai/docker-agent/concepts/agents/).
