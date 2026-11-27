# datalineage-bigquery-asset-impact-analysis

Analyzes the downstream impact (blast radius) using data lineage on Google Cloud when a BigQuery table or view is broken, stale, or modified. Identifies all downstream tables, dashboards, and processes that will be affected. Use when: - Performing a blast radius or impact analysis for a BigQuery table or view. - Assessing the consequences of modifying, deleting, or pausing updates to a BigQuery asset. - Identifying downstream dependencies (tables, dashboards, processes) of a BigQuery asset. Don't use for: - General BigQuery querying or data analysis (use BigQuery-related tools instead). - Non-BigQuery assets (e.g., Cloud Storage files) unless they are part of the BigQuery lineage. - Creating or modifying lineage links directly.

This plugin packages the [`datalineage-bigquery-asset-impact-analysis`](skills/datalineage-bigquery-asset-impact-analysis/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/datalineage-bigquery-asset-impact-analysis) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/datalineage-bigquery-asset-impact-analysis/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install datalineage-bigquery-asset-impact-analysis@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddatalineage-bigquery-asset-impact-analysis),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `datalineage-bigquery-asset-impact-analysis`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
