# managed-airflow-recommendations

Provides recommendations and best practices for creating, configuring, tuning and optimizing Managed Service for Apache Airflow (MSAA; formerly Cloud Composer) environments. Use when the user asks for guidance, recommendations, or best practices on configuring Managed Airflow environments, scaling Airflow environments, preventing workload restarts, or analyzing system health. Don't use for troubleshooting individual DAG or task run failures, authoring DAGs, or migrating DAGs to newer Airflow versions.

This plugin packages the [`managed-airflow-recommendations`](skills/managed-airflow-recommendations/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/managed-airflow-recommendations) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/managed-airflow-recommendations/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install managed-airflow-recommendations@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmanaged-airflow-recommendations),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `managed-airflow-recommendations`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
