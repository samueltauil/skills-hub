# cloud-integrations

Set up, configure, and troubleshoot Grafana Cloud integrations for AWS, Azure, and other cloud providers. Use when the user asks to connect AWS CloudWatch, set up Azure Monitor, configure Confluent Cloud observability, install a Grafana integration, set up hosted exporters, use AWS Firehose for CloudWatch logs, or troubleshoot a cloud integration. Triggers on phrases like "AWS CloudWatch", "Azure Monitor", "Confluent integration", "cloud integration", "hosted exporter", "AWS Firehose", "install integration", "cloud metrics", or "cloud logs".

This plugin packages the [`cloud-integrations`](skills/cloud-integrations/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-cloud/cloud-integrations) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/cloud-integrations/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install cloud-integrations@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcloud-integrations),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `cloud-integrations`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
