# managed-airflow-dag-troubleshooting

Provides guidance for troubleshooting Apache Airflow DAGs (failed DAG runs and task instances) in Managed Service for Apache Airflow (MSAA; formerly Cloud Composer). Use when figuring out reasons for DAG run or task instance failures. Don't use when looking for overall recommendations for Managed Airflow environment performance.

This plugin packages the [`managed-airflow-dag-troubleshooting`](skills/managed-airflow-dag-troubleshooting/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/managed-airflow-dag-troubleshooting) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/managed-airflow-dag-troubleshooting/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install managed-airflow-dag-troubleshooting@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmanaged-airflow-dag-troubleshooting),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `managed-airflow-dag-troubleshooting`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
