# adaptive-metrics

Cut Grafana Cloud Metrics cost by shrinking active-series count with Adaptive Metrics aggregation rules — auto-recommendations from query history, custom exact/regex rules, label-drop config, unused-metric detection, and Alloy remote_write fallback. Use when investigating a high Mimir/Grafana Cloud bill, hunting high-cardinality labels (`pod_uid`, `service_instance_id`, `version`), pre-aggregating counters/gauges, dropping unused metrics, or measuring `grafanacloud_instance_active_series` before/after — even when the user says "reduce cardinality", "too many series", "metrics spend", "active series count is exploding", or "drop the version label" without naming Adaptive Metrics.

This plugin packages the [`adaptive-metrics`](skills/adaptive-metrics/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-cloud/adaptive-metrics) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/adaptive-metrics/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install adaptive-metrics@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dadaptive-metrics),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `adaptive-metrics`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
