# cloud-monitoring-chart-generation

Generates Cloud Monitoring Server-Driven UI (SDUI) Widget and XyChart Protocol Buffer textprotos on Google Cloud from resolved PromQL or ListTimeSeries queries. Use when: - Generating valid google.monitoring.dashboard.v1.Widget textprotos, containing PrometheusQuery or TimeSeriesFilter datasets, for use with the Cloud Monitoring Dashboards API, gcloud CLI, or declarative dashboard definitions. - Synthesizing Server-Driven UI (SDUI) widget titles, axis labels, and plot types for Prometheus or ListTimeSeries queries. Don't use for: - Metric discovery or PromQL query generation. For those tasks, use the cloud-monitoring-metric-selection or cloud-monitoring-promql-query skills.

This plugin packages the [`cloud-monitoring-chart-generation`](skills/cloud-monitoring-chart-generation/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/cloud-monitoring-chart-generation) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/cloud-monitoring-chart-generation/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install cloud-monitoring-chart-generation@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcloud-monitoring-chart-generation),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `cloud-monitoring-chart-generation`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
