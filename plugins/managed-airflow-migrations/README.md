# managed-airflow-migrations

Provides guidance for migrating Apache Airflow DAGs in Managed Service for Apache Airflow (MSAA; formerly Cloud Composer). Covers migration to Airflow 2.11.1 (MSAA Gen 2 and 3) and Airflow 3 (MSAA Gen 3), including environment inspection, GCS download/upload and scanning patterns for breaking changes. Use when migrating the DAG code to newer Airflow version. Don't use when checking DAG run failures unrelated to code migration.

This plugin packages the [`managed-airflow-migrations`](skills/managed-airflow-migrations/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/managed-airflow-migrations) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/managed-airflow-migrations/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install managed-airflow-migrations@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmanaged-airflow-migrations),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `managed-airflow-migrations`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
