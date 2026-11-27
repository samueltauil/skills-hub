# assistant-mcp

Connect AI coding agents (Claude Code, Cursor, VS Code, OpenAI Codex) to Grafana Cloud via the `mcp-grafana` Model Context Protocol server. Installs the server with `go install`, generates a Grafana service-account token, wires `~/.claude/settings.json` or `~/.cursor/mcp.json` with the `command` + `env` block, runs `--disable-write` for safer read-only sessions, switches to SSE transport for team-shared / VS Code setups, and verifies with `/mcp` + a `list_datasources` round-trip. Use when connecting Claude Code to Grafana, setting up MCP for Grafana, configuring the Grafana MCP server, using Grafana tools in Cursor/VS Code, querying Grafana from an AI agent, sharing the MCP server across a team — even when the user says "give my agent Grafana access", "let Claude see my metrics", or "Cursor + Grafana" without saying "MCP".

This plugin packages the [`assistant-mcp`](skills/assistant-mcp/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-cloud/assistant-mcp) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/assistant-mcp/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install assistant-mcp@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dassistant-mcp),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `assistant-mcp`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
