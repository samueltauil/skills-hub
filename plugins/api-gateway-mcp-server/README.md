# api-gateway-mcp-server

Configures Google Cloud API Gateway to act as a remote Model Context Protocol (MCP) server (Public Preview) that exposes REST APIs as agent tools over HTTP (POST /mcp). Use when exposing an API Gateway API as MCP tools, migrating OpenAPI 2.0 specs to OpenAPI 3.x for MCP, annotating specs with x-google-api-management.mcp and x-google-mcp-tool, securing tools/list with JWTs or API keys, connecting Google ADK (McpToolset) or Apigee API hub and Agent Registry, or troubleshooting MCP JSON-RPC errors (-32601, -32602, -32000), /mcp HTTP 404 or 405 errors, and MCP errors from api-configs create. Do not use for a migration without MCP or another OpenAPI error from api-configs create (use api-gateway-openapi-spec-authoring), API key, JWT, or quota setup for REST only (use api-gateway-backend-security-and-rate-limiting), failing non-MCP requests (use api-gateway-troubleshooting), Apigee X proxy bundles, outbound LLM model routing, or GKE Gateway API.

This plugin packages the [`api-gateway-mcp-server`](skills/api-gateway-mcp-server/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/api-gateway-mcp-server) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/api-gateway-mcp-server/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install api-gateway-mcp-server@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dapi-gateway-mcp-server),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `api-gateway-mcp-server`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
