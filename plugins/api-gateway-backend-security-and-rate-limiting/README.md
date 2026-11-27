# api-gateway-backend-security-and-rate-limiting

Secures and rate limits backend services behind Google Cloud API Gateway across OpenAPI 2.0 and OpenAPI 3.x API configurations, including MCP-enabled gateways. Use when configuring API key or JWT authentication, locking down Cloud Run or Cloud Run functions backends with a gateway service account, reading authenticated claims from X-Apigateway-Api-Userinfo, setting per-project request quotas, or changing quota metrics without the HTTP 500 "Failed to call Service Control Quota" error on older gateways. Do not use for finding the cause of failing requests from gateway logs, such as an unexplained HTTP 429 or 5xx (use api-gateway-troubleshooting), writing or migrating a whole spec (use api-gateway-openapi-spec-authoring), MCP tool setup (use api-gateway-mcp-server), Apigee, GKE Gateway API, Cloud Load Balancing custom domain setup, or LLM model routing.

This plugin packages the [`api-gateway-backend-security-and-rate-limiting`](skills/api-gateway-backend-security-and-rate-limiting/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/api-gateway-backend-security-and-rate-limiting) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/api-gateway-backend-security-and-rate-limiting/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install api-gateway-backend-security-and-rate-limiting@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dapi-gateway-backend-security-and-rate-limiting),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `api-gateway-backend-security-and-rate-limiting`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
