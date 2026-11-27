# api-gateway-openapi-spec-authoring

Writes, migrates, and fixes OpenAPI specs for Google Cloud API Gateway. Use when converting an OpenAPI 2.0 (Swagger) spec to OpenAPI 3.x, writing a new OpenAPI 3.x spec, or fixing a failed "gcloud api-gateway api-configs create", such as "extension is only supported in OpenAPI 2.x". Also use when quotas set with x-google-quota are never enforced, or when a backend receives path parameters as query parameters. Don't use for adding or debugging MCP tools (use api-gateway-mcp-server), adding or changing API key, JWT, or quota settings in a working spec, or backend lockdown (use api-gateway-backend-security-and-rate-limiting), failing requests or service account and concurrency errors (use api-gateway-troubleshooting), Cloud Endpoints, Apigee, or GKE Gateway API.

This plugin packages the [`api-gateway-openapi-spec-authoring`](skills/api-gateway-openapi-spec-authoring/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/api-gateway-openapi-spec-authoring) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/api-gateway-openapi-spec-authoring/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install api-gateway-openapi-spec-authoring@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dapi-gateway-openapi-spec-authoring),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `api-gateway-openapi-spec-authoring`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
