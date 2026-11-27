# generate-custom-instructions-from-codebase

Migration and code evolution instructions generator for GitHub Copilot. Analyzes differences between two project versions (branches, commits, or releases) to create precise instructions allowing Copilot to maintain consistency during technology migrations, major refactoring, or framework version upgrades.

This plugin packages the [`generate-custom-instructions-from-codebase`](skills/generate-custom-instructions-from-codebase/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/generate-custom-instructions-from-codebase) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/generate-custom-instructions-from-codebase/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install generate-custom-instructions-from-codebase@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgenerate-custom-instructions-from-codebase),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `generate-custom-instructions-from-codebase`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
