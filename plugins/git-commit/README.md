# git-commit

Use this skill when the user wants to make a Git commit or split changes into more than one commit. Also use it when the user types "/commit" or asks for a conventional commit. The skill examines the diff, stages the related files, writes a Conventional Commits message, and runs git commit. Do not use it when the user wants only a commit message and no commit. Do not use it to push, open a pull request, rebase, or change the commit history.

This plugin packages the [`git-commit`](skills/git-commit/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/git-commit) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/git-commit/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install git-commit@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgit-commit),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `git-commit`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
