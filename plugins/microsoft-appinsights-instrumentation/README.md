# microsoft-appinsights-instrumentation

Guidance for instrumenting webapps with Azure Application Insights. Provides telemetry patterns, SDK setup, and configuration references. WHEN: how to instrument app, App Insights SDK, telemetry patterns, what is App Insights, Application Insights guidance, instrumentation examples, APM best practices.

This plugin packages the [`appinsights-instrumentation`](skills/appinsights-instrumentation/SKILL.md) skill from
[microsoft/azure-skills](https://github.com/microsoft/azure-skills/tree/main/.github/plugins/azure-skills/skills/appinsights-instrumentation) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/microsoft-appinsights-instrumentation/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install microsoft-appinsights-instrumentation@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmicrosoft-appinsights-instrumentation),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `microsoft-appinsights-instrumentation`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[microsoft/azure-skills](https://github.com/microsoft/azure-skills).
