# playwright-interactive

Persistent browser and Electron interaction through `js_repl` for fast iterative UI debugging.

This plugin packages the [`playwright-interactive`](skills/playwright-interactive/SKILL.md) skill from
[openai/skills](https://github.com/openai/skills/tree/main/skills/.curated/playwright-interactive) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/playwright-interactive/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install playwright-interactive@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dplaywright-interactive),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `playwright-interactive`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[openai/skills](https://github.com/openai/skills).
