# database-observability

Set up Grafana Cloud Database Observability for MySQL and PostgreSQL — enables `pg_stat_statements` / Performance Schema, creates a least-privilege monitoring user, configures the `database_observability.postgres` / `database_observability.mysql` Alloy components, ships query samples + visual explain plans + RED metrics + schema details to Grafana Cloud, and correlates slow queries with application traces via `db.statement` / `db.system` OTel attributes. Use when monitoring database performance, diagnosing slow queries, setting up DB observability for RDS / Aurora / Cloud SQL / Azure Database / self-managed instances, correlating DB metrics with APM, or alerting on query latency — even when the user says "my database is slow", "find the slow queries", or "monitor RDS" without saying "observability".

This plugin packages the [`database-observability`](skills/database-observability/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-cloud/database-observability) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/database-observability/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install database-observability@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddatabase-observability),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `database-observability`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
