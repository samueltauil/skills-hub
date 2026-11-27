# cloudflare-app-bootstrap

Get a Cloudflare Workers app to a working local request by connecting its bindings, secrets, and initial data, then verifying real application behavior. Use for app setup or onboarding after the project exists; use frameworks-on-cloudflare or cf-cli to create or configure the project, and wrangler or cf-cli for isolated commands.

This plugin packages the [`cloudflare-app-bootstrap`](skills/cloudflare-app-bootstrap/SKILL.md) skill from
[cloudflare/skills](https://github.com/cloudflare/skills/tree/main/skills/cloudflare-app-bootstrap) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/cloudflare-app-bootstrap/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install cloudflare-app-bootstrap@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcloudflare-app-bootstrap),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `cloudflare-app-bootstrap`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[cloudflare/skills](https://github.com/cloudflare/skills).
