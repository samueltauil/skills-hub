# durable-objects

Build, debug, or review Cloudflare Durable Objects code for persistent state and coordination.

This plugin packages the [`durable-objects`](skills/durable-objects/SKILL.md) skill from
[cloudflare/skills](https://github.com/cloudflare/skills/tree/main/skills/durable-objects) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/durable-objects/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install durable-objects@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddurable-objects),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `durable-objects`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[cloudflare/skills](https://github.com/cloudflare/skills).
