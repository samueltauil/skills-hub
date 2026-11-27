# service-reliability

Design and operate service reliability targets in Elastic Observability: choose an SLI type and a defensible target, pick a time window and budgeting method, create and maintain SLOs through the Kibana API, attach burn-rate alert rules, and decide when an SLO is the wrong instrument and a threshold rule, anomaly job, or synthetics monitor is right. Use when defining or reviewing SLOs and error budgets, tuning burn-rate alerting, reducing alert noise, or setting up availability monitoring for a user-facing endpoint.

This plugin packages the [`observability-service-reliability`](skills/observability-service-reliability/SKILL.md) skill from
[elastic/agent-skills](https://github.com/elastic/agent-skills/tree/main/skills/observability/service-reliability) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/service-reliability/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install service-reliability@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dservice-reliability),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `service-reliability`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[elastic/agent-skills](https://github.com/elastic/agent-skills).
