# cloud-monitoring-alert-configuration

Configures Cloud Monitoring alerting policies using Terraform and PromQL across Cloud Run, Google Kubernetes Engine (GKE), Compute Engine, AI Hypercomputer reservations, Vertex AI Agent Engine, and generic Google Cloud resources. Use when creating, reviewing, migrating, or deduplicating Terraform alerting policies for latency, traffic, error rates, saturation, host or reservation maintenance, GPU XID insights, or AI agent telemetry. Don't use for standalone PromQL query authoring without alerting, log querying, or billing cost audits.

This plugin packages the [`cloud-monitoring-alert-configuration`](skills/cloud-monitoring-alert-configuration/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/cloud-monitoring-alert-configuration) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/cloud-monitoring-alert-configuration/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install cloud-monitoring-alert-configuration@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcloud-monitoring-alert-configuration),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `cloud-monitoring-alert-configuration`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
