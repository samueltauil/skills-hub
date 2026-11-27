# dbt-sf-to-bq-translator

Translates Snowflake dbt SQL models to Standardized BigQuery SQL. Handles SQL compilation, Jinja macro placeholder masking, BigQuery Translation Service migration workflows, AST-based config transformations, explicit type casting, JSON extraction standardization, and deduplication. Use when migrating Snowflake dbt pipelines or models to BigQuery on Google Cloud. Don't use for generic BigQuery queries or non-Snowflake SQL migrations.

This plugin packages the [`dbt-sf-to-bq-translator`](skills/dbt-sf-to-bq-translator/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/dbt-sf-to-bq-translator) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/dbt-sf-to-bq-translator/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install dbt-sf-to-bq-translator@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddbt-sf-to-bq-translator),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `dbt-sf-to-bq-translator`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
