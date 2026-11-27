# google-cloud-networking-observability

Investigates Google Cloud networking issues by analyzing GCP logs, metrics, and diagnostics. Use when investigating dropped network traffic, packet drops, drop reasons, VPC Flow Logs (including Private Service Connect / PSC, serverless / App Engine Direct VPC, and cost estimation), Cloud NAT, firewall or threat logs, VPN metrics/tunnels, or Connectivity Tests for path diagnostics. Don't use for generic VM management or non-observability tasks.

This plugin packages the [`google-cloud-networking-observability`](skills/google-cloud-networking-observability/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/google-cloud-networking-observability) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/google-cloud-networking-observability/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install google-cloud-networking-observability@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgoogle-cloud-networking-observability),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `google-cloud-networking-observability`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
