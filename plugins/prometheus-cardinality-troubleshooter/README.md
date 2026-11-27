# prometheus-cardinality-troubleshooter

Diagnostic guide for active Prometheus cardinality problems — slow queries, OOMing Prometheus, high Grafana Cloud Active Series or DPM bills, "too many samples" ingest errors, series churn, or rapid memory growth. Walks through tsdb status endpoints, per-metric and per-label drill-downs, common-culprit galleries, and remediation paths. Use when the user is *currently experiencing* a cardinality fire. For preventing cardinality issues at the source, route to prometheus-label-strategy. For post-ingest aggregation, route to adaptive-metrics. For DPM-specific analysis, route to dpm-finder.

This plugin packages the [`prometheus-cardinality-troubleshooter`](skills/prometheus-cardinality-troubleshooter/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-cloud/prometheus-cardinality-troubleshooter) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/prometheus-cardinality-troubleshooter/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install prometheus-cardinality-troubleshooter@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dprometheus-cardinality-troubleshooter),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `prometheus-cardinality-troubleshooter`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
