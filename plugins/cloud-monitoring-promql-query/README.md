# cloud-monitoring-promql-query

Generates valid PromQL queries from Cloud Monitoring metric descriptors and resource parameters. Use when asked to create, generate, write, or format PromQL queries, PromQL strings, or PromQL aggregations for Cloud Monitoring metrics and resources. Don't use for raw metric discovery or metric selection.

This plugin packages the [`cloud-monitoring-promql-query`](skills/cloud-monitoring-promql-query/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/cloud-monitoring-promql-query) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/cloud-monitoring-promql-query/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install cloud-monitoring-promql-query@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcloud-monitoring-promql-query),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `cloud-monitoring-promql-query`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
