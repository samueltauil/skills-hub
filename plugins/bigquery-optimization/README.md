# bigquery-optimization

Provides workflows to optimize BigQuery environments (capacity planning, editions), storage assets (partitioning, clustering, storage lifecycles, billing models), and SQL queries. Use when optimizing cost, modeling Edition migrations, rightsizing reservations, evaluating logical vs. physical storage, designing table partitioning/clustering, generating table DDL, migrating unpartitioned tables, managing partition expiration, optimizing individual SQL queries, or evaluating acceleration structures (search indexes, materialized views, BI Engine). Do not use for raw usage reporting (use bigquery-observability), query execution plan analysis, error troubleshooting, or diagnosing why a specific job was slow (use bigquery-troubleshooting).

This plugin packages the [`bigquery-optimization`](skills/bigquery-optimization/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/bigquery-optimization) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/bigquery-optimization/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install bigquery-optimization@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dbigquery-optimization),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `bigquery-optimization`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
