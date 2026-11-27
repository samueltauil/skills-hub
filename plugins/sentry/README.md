# sentry

Use when the user asks to inspect Sentry issues or events, summarize recent production errors, or pull basic Sentry health data via the Sentry CLI; perform read-only queries using the `sentry` command.

This plugin packages the [`sentry`](skills/sentry/SKILL.md) skill from
[openai/skills](https://github.com/openai/skills/tree/main/skills/.curated/sentry) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/sentry/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install sentry@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsentry),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `sentry`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[openai/skills](https://github.com/openai/skills).
