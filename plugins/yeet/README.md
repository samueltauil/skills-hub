# yeet

Use only when the user explicitly asks to stage, commit, push, and open a GitHub pull request in one flow using the GitHub CLI (`gh`).

This plugin packages the [`yeet`](skills/yeet/SKILL.md) skill from
[openai/skills](https://github.com/openai/skills/tree/main/skills/.curated/yeet) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/yeet/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install yeet@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dyeet),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `yeet`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[openai/skills](https://github.com/openai/skills).
