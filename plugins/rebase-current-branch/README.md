# rebase-current-branch

Rebase the currently checked out feature branch onto the latest upstream default branch. Use when asked to update a branch with main or master, rebase the current branch onto the default branch, or sync a feature branch before review. Detects whether the repository uses main or master and guides safe conflict handling.

This plugin packages the [`rebase-current-branch`](skills/rebase-current-branch/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/rebase-current-branch) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/rebase-current-branch/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install rebase-current-branch@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Drebase-current-branch),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `rebase-current-branch`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
