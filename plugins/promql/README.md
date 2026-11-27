# promql

Write, validate, and optimize PromQL for Prometheus / Grafana Mimir / Grafana Cloud Metrics. Covers `rate` vs `irate` vs `increase`, label matchers and regex, `sum / avg / topk / by / without` aggregation, classic + native `histogram_quantile`, ratios with divide-by-zero guards, `absent` / `changes` for staleness, time offsets and `predict_linear`, recording-rule naming, SLO + burn-rate math, and a cardinality-hunting playbook. Use when writing a metric query, fixing wrong p95s, building an error-budget alert, debugging "query is slow", finding the noisy label that blew up cardinality, or migrating a dashboard query to a recording rule — even when the user says "calculate the error rate", "p99 latency", "sum by service", "why is this query slow", or "what's filling Mimir" without naming PromQL.

This plugin packages the [`promql`](skills/promql/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-core/promql) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/promql/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install promql@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpromql),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `promql`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
