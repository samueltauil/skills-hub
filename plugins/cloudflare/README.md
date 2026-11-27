# cloudflare

Discover and choose Cloudflare products for apps, APIs, AI agents, storage, networking, and security. Use for architecture and product selection, including when the user describes a need without naming a Cloudflare product; then find the relevant skill or documentation. Also use when a Cloudflare-proxied site shows a Cloudflare error page, a `52x` status, a 1xxx error code, or a Cloudflare `403`, to decide whether to fix Cloudflare configuration or the origin.

This plugin packages the [`cloudflare`](skills/cloudflare/SKILL.md) skill from
[cloudflare/skills](https://github.com/cloudflare/skills/tree/main/skills/cloudflare) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/cloudflare/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install cloudflare@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcloudflare),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `cloudflare`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[cloudflare/skills](https://github.com/cloudflare/skills).
