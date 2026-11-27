# bigquery-observability

Provides data-retrieval best practices, tool selection guidance, and performant SQL query syntax for BigQuery telemetry across INFORMATION_SCHEMA, Cloud Monitoring, and the REST API. Use when the telemetry to fetch is already known, selecting telemetry tools, writing performant INFORMATION_SCHEMA queries, retrieving telemetry for diagnosing single-job performance bottlenecks, investigating slot contention, job concurrency and queue latency, analyzing reservation capacity, utilization and autoscaling saturation, or auditing capacity-based and on-demand compute and storage resource billable usage. Don't use for root-cause diagnosis or symptom troubleshooting when the cause is unknown (use bigquery-troubleshooting first), or for writing or optimizing business logic SQL (use bigquery-optimization).

This plugin packages the [`bigquery-observability`](skills/bigquery-observability/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/bigquery-observability) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/bigquery-observability/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install bigquery-observability@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dbigquery-observability),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `bigquery-observability`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
