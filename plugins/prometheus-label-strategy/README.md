# prometheus-label-strategy

Expert evaluator for Prometheus label strategy on Grafana Cloud. Audits, designs, and improves label schemas using cardinality scoring, access-pattern alignment, static vs. dynamic label rules, histogram bucket discipline, and instrumentation hygiene. Prevents high cardinality at the source — in application code and scrape target labels — without dropping labels that make series unique (which breaks the data). For reducing the cost of series already in Grafana Cloud, routes to the adaptive-metrics skill. Use when the user asks to evaluate, audit, design, or improve Prometheus labels — or asks how to prevent high cardinality at the source. For "why is my Prometheus slow / expensive right now" triage, see prometheus-cardinality-troubleshooter.

This plugin packages the [`prometheus-label-strategy`](skills/prometheus-label-strategy/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-cloud/prometheus-label-strategy) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/prometheus-label-strategy/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install prometheus-label-strategy@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dprometheus-label-strategy),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `prometheus-label-strategy`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
