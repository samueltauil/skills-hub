# api-breaking-change-detector

Cross-references C# Web API controllers/DTOs against their TypeScript/JavaScript consumers (React, Angular, Vue, Svelte, Node.js, or hand-written/auto-generated HTTP clients like Fetch, Axios, NSwag) to catch contract drift in both directions: backend changes that break client applications (renamed/removed JSON keys, new required parameters, status code shifts) and frontend code sending fields the backend no longer reads. Works directly against source code, not exported OpenAPI spec files. Use when the user asks to check for breaking API changes, verify frontend/backend contract sync, or audit a DTO/controller change against its TypeScript/JS consumers before merging. Not for generating new API code from a spec (see openapi-to-application-code) or scaffolding new endpoints (see aspnet-minimal-api-openapi).

This plugin packages the [`api-breaking-change-detector`](skills/api-breaking-change-detector/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/api-breaking-change-detector) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/api-breaking-change-detector/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install api-breaking-change-detector@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dapi-breaking-change-detector),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `api-breaking-change-detector`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
