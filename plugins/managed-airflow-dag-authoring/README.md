# managed-airflow-dag-authoring

Provides guidance for authoring Apache Airflow DAGs in Managed Service for Apache Airflow (MSAA; formerly Cloud Composer). Covers environment context discovery, Airflow 2 vs 3 compatibility, authoring best practices, and local/remote validation processes. Use when creating or extending an Airflow DAG. Don't use when authoring Python code unrelated to Airflow DAGs.

This plugin packages the [`managed-airflow-dag-authoring`](skills/managed-airflow-dag-authoring/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/managed-airflow-dag-authoring) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/managed-airflow-dag-authoring/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install managed-airflow-dag-authoring@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmanaged-airflow-dag-authoring),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `managed-airflow-dag-authoring`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
