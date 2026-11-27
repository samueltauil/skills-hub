# bigquery-migration-metadata-extractor

Extracts database catalog metadata and query logs from data warehouses by running the DWH migration extractor locally or on a temporary Google Cloud VM through the BigQuery Migration Cloud Extractor (credentials held in Secret Manager), and inspects extracted `.zip` archives to report object and volume statistics. Use when extracting database metadata or query logs from Snowflake, Redshift, Teradata, Oracle, PostgreSQL, SQL Server, Hive, etc., deciding between local and cloud (Cloud Extractor) extraction, or inspecting extracted dwh-migration-*.zip archives to print post-extraction statistics. Don't use for SQL dialect translation (use bigquery-migration-sql-translator), exporting table data to Parquet or CSV files (such as Snowflake `COPY INTO` unloads) or loading it into BigQuery (use the BigQuery Data Transfer Service or bigquery-basics), or validating migrated data.

This plugin packages the [`bigquery-migration-metadata-extractor`](skills/bigquery-migration-metadata-extractor/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/bigquery-migration-metadata-extractor) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/bigquery-migration-metadata-extractor/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install bigquery-migration-metadata-extractor@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dbigquery-migration-metadata-extractor),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `bigquery-migration-metadata-extractor`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
