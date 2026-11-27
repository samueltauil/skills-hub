# bigquery-migration-data-loader

Provisions BigQuery datasets, ingests staged Parquet files directly into native BigQuery tables by using bq load, and deploys already-translated views from local or Cloud Storage BigQuery Migration Service (BQMS) translation outputs. Use when provisioning target BigQuery datasets for warehouse migrations, batch loading staged Parquet files into native BigQuery tables by using bq load, auditing loaded table row counts, or deploying already-translated BigQuery views into a target dataset. Don't use for extracting source database catalog metadata, translating SQL queries, views, stored procedures, or DDL schemas to GoogleSQL (use bigquery-migration-sql-translator), exporting or unloading source database tables (such as Snowflake, Databricks, Teradata, or Oracle) to Parquet on Cloud Storage, or running post-migration cross-database data validation.

This plugin packages the [`bigquery-migration-data-loader`](skills/bigquery-migration-data-loader/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/bigquery-migration-data-loader) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/bigquery-migration-data-loader/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install bigquery-migration-data-loader@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dbigquery-migration-data-loader),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `bigquery-migration-data-loader`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
