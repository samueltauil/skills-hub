# sentry-pr-screenshots

Capture screenshots of the Sentry UI in a web browser, lay them out in a pull request description as before/after tables, and upload them with `gh --attach`.

This plugin packages the [`pr-screenshots`](skills/pr-screenshots/SKILL.md) skill from
[getsentry/skills](https://github.com/getsentry/skills/tree/main/skills/pr-screenshots) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/sentry-pr-screenshots/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install sentry-pr-screenshots@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsentry-pr-screenshots),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `sentry-pr-screenshots`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[getsentry/skills](https://github.com/getsentry/skills).
