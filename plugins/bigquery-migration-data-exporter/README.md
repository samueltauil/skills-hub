# bigquery-migration-data-exporter

Generates type-safe, schema-aligned database data export SQL files (.sql) for Snowflake, Databricks, Teradata, Oracle, and PostgreSQL directly from BigQuery Migration Service (BQMS) translation_output/metadata configs, exporting into target file formats (such as Parquet). Use when generating source database export SQL scripts for BigQuery ingestion without connecting to the source database. Don't use for executing SQL against source databases or streaming/staging exported files, extracting source database catalog metadata, translating SQL queries or DDL schemas (use bigquery-migration-sql-translator), loading staged Parquet files into BigQuery, or running post-migration data validation.

This plugin packages the [`bigquery-migration-data-exporter`](skills/bigquery-migration-data-exporter/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/bigquery-migration-data-exporter) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/bigquery-migration-data-exporter/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install bigquery-migration-data-exporter@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dbigquery-migration-data-exporter),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `bigquery-migration-data-exporter`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
