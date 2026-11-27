# cloud-monitoring-metric-selection

Retrieve, query, and identify relevant Cloud Monitoring metric descriptors on Google Cloud for a service or resource (such as Compute Engine, Spanner, BigQuery, Cloud Run, Cloud SQL, Pub/Sub, Cloud Storage, etc.). Use when asked to find, list, search, or discover GCP metric types, names, kind/value schemas, or descriptors.

This plugin packages the [`cloud-monitoring-metric-selection`](skills/cloud-monitoring-metric-selection/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/cloud-monitoring-metric-selection) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/cloud-monitoring-metric-selection/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install cloud-monitoring-metric-selection@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcloud-monitoring-metric-selection),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `cloud-monitoring-metric-selection`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
