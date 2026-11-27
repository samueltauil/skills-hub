# prometheus

Prometheus and Grafana Cloud Metrics overview including PromQL query language, Metrics Drilldown, alerting, recording rules, and integration patterns. Use when working with Prometheus, writing PromQL queries, configuring alerting, or discussing metrics architecture and best practices.

This plugin packages the [`prometheus`](skills/prometheus/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-lgtm/prometheus) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/prometheus/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install prometheus@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dprometheus),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `prometheus`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
