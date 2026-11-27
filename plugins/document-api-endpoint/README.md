# document-api-endpoint

Document and type a Sentry API endpoint. Write or fix @extend_schema decorators, specify response TypedDicts, type request parameters, correct type drift between the declared schema and the runtime response, and validate the generated spec. Use when asked to "document an endpoint", "add OpenAPI docs", "add/fix @extend_schema", "type an endpoint response", "fix the response type", "fix type drift", "reuse a response type", "split an overloaded endpoint", "specify the response schema", "add a TypedDict response", "migrate a legacy api-docs path", "fix a parameter type", or "make an endpoint public" / "promote an endpoint" (promotion is one section here).

This plugin packages the [`document-api-endpoint`](skills/document-api-endpoint/SKILL.md) skill from
[getsentry/skills](https://github.com/getsentry/skills/tree/main/skills/document-api-endpoint) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/document-api-endpoint/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install document-api-endpoint@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddocument-api-endpoint),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `document-api-endpoint`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[getsentry/skills](https://github.com/getsentry/skills).
