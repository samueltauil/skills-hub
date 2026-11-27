# bigquery-migration-validator

Validates that tables migrated to BigQuery match their source (Teradata, Snowflake, Oracle, Redshift, Databricks, PostgreSQL, SQL Server, MySQL, MariaDB, Hive, Impala, Vertica) with the BigQuery Migration Service (BQMS) validation tool: schema and data type comparison, column aggregate comparison, and row-level data comparison. Use when generating or editing a validation config, running a validation, choosing sampling or partitioning, fixing connection or driver errors, or investigating validation results in BigQuery and Cloud Storage to decide which mismatches to fix. Don't use for SQL translation (use bigquery-migration-sql-translator), extracting source database catalog metadata or query logs, generating SQL scripts (such as COPY INTO) or exporting or unloading source tables to Parquet on Cloud Storage, loading staged files into BigQuery (such as bq load), or general BigQuery query failures and tuning (use bigquery-troubleshooting or bigquery-optimization).

This plugin packages the [`bigquery-migration-validator`](skills/bigquery-migration-validator/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/bigquery-migration-validator) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/bigquery-migration-validator/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install bigquery-migration-validator@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dbigquery-migration-validator),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `bigquery-migration-validator`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
