# code-review

Perform code reviews following Sentry engineering practices. Use when reviewing pull requests, examining code changes, or providing feedback on code quality. Covers security, performance, testing, and design review.

This plugin packages the [`code-review`](skills/code-review/SKILL.md) skill from
[getsentry/skills](https://github.com/getsentry/skills/tree/main/skills/code-review) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/code-review/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install code-review@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcode-review),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `code-review`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[getsentry/skills](https://github.com/getsentry/skills).
