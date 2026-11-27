# cost-management

Cut your Grafana Cloud bill by attributing spend to teams and reducing telemetry volume. Covers FOCUS-compliant billing dashboards, cost-attribution labels in Alloy, Adaptive Metrics (cardinality reduction), Adaptive Logs (drop/sample), Adaptive Traces (tail sampling), usage alerts, and an optimization checklist. Use when investigating a high Grafana Cloud bill, attributing observability cost to a team or service, reducing active series / log bytes / trace spans, or setting up usage / quota alerts — even when the user says "our Grafana bill is too high", "who's burning the most metrics", "drop debug logs", "sample our traces", or "alert me before we hit quota" without naming Cost Management.

This plugin packages the [`cost-management`](skills/cost-management/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-cloud/cost-management) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/cost-management/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install cost-management@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcost-management),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `cost-management`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
