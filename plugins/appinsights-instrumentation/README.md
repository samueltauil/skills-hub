# appinsights-instrumentation

Instrument a webapp to send useful telemetry data to Azure App Insights

This plugin packages the [`appinsights-instrumentation`](skills/appinsights-instrumentation/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/appinsights-instrumentation) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/appinsights-instrumentation/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install appinsights-instrumentation@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dappinsights-instrumentation),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `appinsights-instrumentation`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
