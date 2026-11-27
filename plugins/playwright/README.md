# playwright

Use when the task requires automating a real browser from the terminal (navigation, form filling, snapshots, screenshots, data extraction, UI-flow debugging) via `playwright-cli` or the bundled wrapper script.

This plugin packages the [`playwright`](skills/playwright/SKILL.md) skill from
[openai/skills](https://github.com/openai/skills/tree/main/skills/.curated/playwright) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/playwright/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install playwright@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dplaywright),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `playwright`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[openai/skills](https://github.com/openai/skills).
