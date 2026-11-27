# conventional-branch

Create Git branches following the Conventional Branch specification (feature/, bugfix/, hotfix/, release/, chore/, plus AI agent prefixes ai/, copilot/, cursor/, claude/, codex/). Use when creating a new branch, naming a branch, or checking whether a branch name complies with the spec.

This plugin packages the [`conventional-branch`](skills/conventional-branch/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/conventional-branch) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/conventional-branch/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install conventional-branch@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dconventional-branch),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `conventional-branch`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
