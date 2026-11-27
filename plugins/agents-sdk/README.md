# agents-sdk

Build, debug, or review Cloudflare Agents SDK applications using the agents package.

This plugin packages the [`agents-sdk`](skills/agents-sdk/SKILL.md) skill from
[cloudflare/skills](https://github.com/cloudflare/skills/tree/main/skills/agents-sdk) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/agents-sdk/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install agents-sdk@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dagents-sdk),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `agents-sdk`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[cloudflare/skills](https://github.com/cloudflare/skills).
