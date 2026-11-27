# bigquery-migration-sql-translator

Translates SQL queries, DDL schemas, and stored procedures from legacy database dialects (Teradata, Oracle, Redshift, Snowflake, SparkSQL, HiveQL) to BigQuery GoogleSQL using the BigQuery Migration Service (BQMS) MCP server. Use when translating legacy SQL queries, migrating schemas or metadata zip archives, or configuring BigQuery Migration Service (BQMS) YAML translation settings. Don't use for executing BigQuery queries or managing datasets and tables (use bigquery-basics), diagnosing runtime job errors (use bigquery-troubleshooting), or tuning slot reservations (use bigquery-optimization).

This plugin packages the [`bigquery-migration-sql-translator`](skills/bigquery-migration-sql-translator/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/bigquery-migration-sql-translator) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/bigquery-migration-sql-translator/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install bigquery-migration-sql-translator@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dbigquery-migration-sql-translator),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `bigquery-migration-sql-translator`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
