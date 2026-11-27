# api-gateway-troubleshooting

Diagnoses failing requests and deployment errors on Google Cloud API Gateway. Use when calls through a gateway return 4xx or 5xx errors, including 429 and other quota errors, time out, or fail a CORS preflight; when `api-configs create` fails with a service account, concurrency, or limit error, or `gateways create` or `gateways update` fails; when a custom domain, load balancer, or TLS finding involves a gateway; or when the user asks if Google is at fault. Don't use for Apigee, Cloud Endpoints, or GKE Gateway API. For OpenAPI errors from `api-configs create`, use api-gateway-openapi-spec-authoring; for setting up or changing API keys, JWTs, or quotas, use api-gateway-backend-security-and-rate-limiting; for MCP `/mcp` errors, use api-gateway-mcp-server.

This plugin packages the [`api-gateway-troubleshooting`](skills/api-gateway-troubleshooting/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/api-gateway-troubleshooting) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/api-gateway-troubleshooting/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install api-gateway-troubleshooting@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dapi-gateway-troubleshooting),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `api-gateway-troubleshooting`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
