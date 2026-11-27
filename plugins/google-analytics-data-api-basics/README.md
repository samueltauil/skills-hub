# google-analytics-data-api-basics

Manages Google Analytics reporting data, enables the Analytics Data API via the Cloud CLI, and creates reports using the Google Analytics Data API (v1beta). Use when you need to interact with Google Analytics properties, run customized analytics reports, query metrics (like activeUsers, screenPageViews) and dimensions (like city, date), check metrics and dimensions compatibility, or verify API enablement. Don't use for Google Analytics Admin API operations (e.g., creating properties, managing users) or for front-end tracking installation.

This plugin packages the [`google-analytics-data-api-basics`](skills/google-analytics-data-api-basics/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/analytics/google-analytics-data-api-basics) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/google-analytics-data-api-basics/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install google-analytics-data-api-basics@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgoogle-analytics-data-api-basics),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `google-analytics-data-api-basics`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
