# gke-cost-analysis

Answer natural language questions and perform analysis on GKE cluster and workload costs using BigQuery billing exports, cost allocation data, and live cluster monitoring metrics. Use when querying GKE costs across projects, namespaces, or workloads, analyzing billing reports in BigQuery (`bq`), checking cluster cost budgets (`gcloud billing`), or diagnosing cost drivers like pod requests vs. actual utilization (`kubectl top`). Don't use for applying cost optimization changes, creating rightsizing manifests (VPA/MPA), or selecting ComputeClasses (use gke-cost-optimization instead).

This plugin packages the [`gke-cost-analysis`](skills/gke-cost-analysis/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-cost-analysis) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-cost-analysis/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-cost-analysis@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-cost-analysis),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-cost-analysis`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
