# datalineage-summary

Summarizes data lineage graphs on Google Cloud to help users debug data quality issues and understand data provenance for BigQuery and Cloud Storage. Use when summarizing upstream and downstream data flows, and presenting complex lineage data as an intuitive Markdown report. Don't use for generic BigQuery queries, editing lineage relationships, or downstream deprecation. Don't use for downstream blast-radius impact analysis (use datalineage-bigquery-asset-impact-analysis skill instead).

This plugin packages the [`datalineage-summary`](skills/datalineage-summary/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/datalineage-summary) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/datalineage-summary/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install datalineage-summary@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddatalineage-summary),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `datalineage-summary`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
