# bigquery-troubleshooting

Provides diagnostic workflows and step-by-step root-cause analysis procedures for actively broken, failing, or slow BigQuery jobs, execution graph and query plan stage bottlenecks, system performance issues, or unexpectedly expensive workloads. Use when interpreting symptoms, isolating bottlenecks, diagnosing cost spikes (on-demand query spend, capacity slot autoscaling, storage growth), execution graph stages or substep variables, identifying root causes, and determining remediation steps. Don't use for writing or optimizing SQL, proactive capacity planning, or storage layout design (use bigquery-optimization), or when the user already knows which telemetry they want and just needs the query (use bigquery-observability).

This plugin packages the [`bigquery-troubleshooting`](skills/bigquery-troubleshooting/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/bigquery-troubleshooting) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/bigquery-troubleshooting/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install bigquery-troubleshooting@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dbigquery-troubleshooting),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `bigquery-troubleshooting`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
