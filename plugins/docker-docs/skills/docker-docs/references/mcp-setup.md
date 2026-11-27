# Docker docs MCP server setup and diagnostics

Use this reference only when the user explicitly asks to add, configure, or
troubleshoot the Docker docs MCP server. During an ordinary documentation
question, a missing search tool is not a setup request. Use the fallback in
`SKILL.md` instead.

## Server facts

- Endpoint: `https://ai-backend-service.docker.com/mcp`
- Transport: Streamable HTTP. No authentication or session setup is
  required.
- Tool: `search_docker_docs`. It takes one required string argument,
  `message`, and returns `documents` with `content` excerpts and
  `metadata.source` URLs. It is read-only.
- Recommended server name: `docker-docs`.

## Bundled with the Docker skills plugin

Installing the Docker skills plugin from the Claude Code, Codex, Cursor, or
GitHub Copilot CLI marketplace, or as a Gemini CLI extension, also registers
this server as `docker-docs`. If the plugin is installed but the server is
missing, check that the plugin is enabled and that the client loaded its MCP
servers, before you add the server by hand. A manually added server with the
same URL duplicates the plugin's server.

The skills CLI, Docker Sandboxes skill installation, and manual copies
install skills only. Configure the server separately for those.

## Manual configuration

Check the user's client and its current MCP documentation before you
recommend a command. Then use the matching form:

```bash
# Claude Code
claude mcp add --transport http docker-docs https://ai-backend-service.docker.com/mcp

# Codex
codex mcp add docker-docs --url https://ai-backend-service.docker.com/mcp

# Gemini CLI
gemini mcp add --transport http docker-docs https://ai-backend-service.docker.com/mcp
```

For clients configured with an `mcpServers` JSON file, such as a project
`.mcp.json` or Cursor's `mcp.json`:

```json
{
  "mcpServers": {
    "docker-docs": {
      "type": "http",
      "url": "https://ai-backend-service.docker.com/mcp"
    }
  }
}
```

For Docker Agent, add the server as a remote MCP toolset in `agent.yaml`.
`docker-agent-config` owns that file format.

## Diagnose a server that doesn't work

1. Confirm the client lists the server and shows it as enabled or connected,
   using its MCP list command or settings view.
2. Confirm the endpoint is reachable from the machine running the client:

   ```bash
   curl -fsS -X POST https://ai-backend-service.docker.com/mcp \
     -H 'Content-Type: application/json' \
     -H 'Accept: application/json, text/event-stream' \
     -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
   ```

   A JSON response that lists the search tool means the server is healthy.
   An HTTP 403 from a proxy or firewall means the network blocks the
   endpoint. Report that and use the fallback. Don't try to bypass it.
3. Check for organization policy that blocks remote MCP servers, such as
   managed client settings or a sandbox MCP or network policy.
4. Report success only after the client shows the tool or a search call
   returns results. Don't claim it works without that evidence.

Adding or editing configuration doesn't make the tool callable in the current
session. Most clients load MCP servers at startup. Tell the user which
client needs a new session, or a reload, before the tool appears.

Change configuration only when the user explicitly asks for it. Never add the
server, edit settings, or ask for a restart just to answer a documentation
question.
