# find-bugs

Find bugs, security vulnerabilities, and code quality issues in local branch changes. Use when asked to review changes, find bugs, security review, or audit code on the current branch.

This plugin packages the [`find-bugs`](skills/find-bugs/SKILL.md) skill from
[getsentry/skills](https://github.com/getsentry/skills/tree/main/skills/find-bugs) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/find-bugs/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install find-bugs@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dfind-bugs),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `find-bugs`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[getsentry/skills](https://github.com/getsentry/skills).
