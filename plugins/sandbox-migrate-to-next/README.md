# sandbox-migrate-to-next

Migrate Cloudflare Sandbox apps from stable @cloudflare/sandbox to @cloudflare/sandbox@next (SDK 1.0 preview). Use sandbox-next for apps already on the preview.

This plugin packages the [`sandbox-migrate-to-next`](skills/sandbox-migrate-to-next/SKILL.md) skill from
[cloudflare/skills](https://github.com/cloudflare/skills/tree/main/skills/sandbox-migrate-to-next) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/sandbox-migrate-to-next/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install sandbox-migrate-to-next@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsandbox-migrate-to-next),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `sandbox-migrate-to-next`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[cloudflare/skills](https://github.com/cloudflare/skills).
