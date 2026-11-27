# ruff-recursive-fix

Run Ruff checks with optional scope and rule overrides, apply safe and unsafe autofixes iteratively, review each change, and resolve remaining findings with targeted edits or user decisions.

This plugin packages the [`ruff-recursive-fix`](skills/ruff-recursive-fix/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/ruff-recursive-fix) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/ruff-recursive-fix/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install ruff-recursive-fix@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Druff-recursive-fix),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `ruff-recursive-fix`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
