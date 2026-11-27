# commit-message-storyteller

Analyzes git diffs or staged changes and generates narrative commit messages that explain WHY a change was made, not just what changed — following Conventional Commits format. Use when asked to "write a commit message", "describe my changes", "what should I commit this as", or "summarize my diff". Works with git diff output, staged files, or plain descriptions of changes. Does not run git commit; to stage files and make the commit, use the git-commit skill.

This plugin packages the [`commit-message-storyteller`](skills/commit-message-storyteller/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/commit-message-storyteller) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/commit-message-storyteller/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install commit-message-storyteller@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcommit-message-storyteller),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `commit-message-storyteller`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
