# browse-local-sentry

Connects an agent's browser to a local Sentry dev server (dev-ui on *.dev.getsentry.net or the full devserver).

This plugin packages the [`browse-local-sentry`](skills/browse-local-sentry/SKILL.md) skill from
[getsentry/skills](https://github.com/getsentry/skills/tree/main/skills/browse-local-sentry) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/browse-local-sentry/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install browse-local-sentry@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dbrowse-local-sentry),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `browse-local-sentry`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[getsentry/skills](https://github.com/getsentry/skills).
