# k6-trend-analysis

Analyze Grafana Cloud k6 test run trends over time. Detects slow metric drift (e.g., P95 latency creeping up while still passing thresholds), computes headroom to thresholds, flags anomalies, and recommends threshold tightening. Use when the user asks about test performance trends, wants to know if metrics are degrading, asks whether thresholds should be tightened, or wants a health check across recent runs for a specific test. Trigger on phrases like "how is my test trending", "is P95 getting worse", "check for performance regression", "should I tighten thresholds", "are my tests degrading", "show me trends for test X", "analyze my k6 test runs", or "is my test getting slower". Also trigger when a user asks to check all tests in a project -- run this skill once per test and synthesize.

This plugin packages the [`k6-trend-analysis`](skills/k6-trend-analysis/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-k6/k6-trend-analysis) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/k6-trend-analysis/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install k6-trend-analysis@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dk6-trend-analysis),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `k6-trend-analysis`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
