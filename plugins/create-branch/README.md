# create-branch

Create a git branch following Sentry naming conventions. Use when asked to "create a branch", "new branch", "start a branch", "make a branch", "switch to a new branch", or when starting new work on the default branch.

This plugin packages the [`create-branch`](skills/create-branch/SKILL.md) skill from
[getsentry/skills](https://github.com/getsentry/skills/tree/main/skills/create-branch) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/create-branch/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install create-branch@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcreate-branch),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `create-branch`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[getsentry/skills](https://github.com/getsentry/skills).
