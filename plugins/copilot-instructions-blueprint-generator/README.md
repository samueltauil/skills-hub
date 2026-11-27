# copilot-instructions-blueprint-generator

Technology-agnostic blueprint generator for creating comprehensive copilot-instructions.md files that guide GitHub Copilot to produce code consistent with project standards, architecture patterns, and exact technology versions by analyzing existing codebase patterns and avoiding assumptions.

This plugin packages the [`copilot-instructions-blueprint-generator`](skills/copilot-instructions-blueprint-generator/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/copilot-instructions-blueprint-generator) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/copilot-instructions-blueprint-generator/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install copilot-instructions-blueprint-generator@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcopilot-instructions-blueprint-generator),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `copilot-instructions-blueprint-generator`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
