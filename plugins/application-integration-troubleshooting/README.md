# application-integration-troubleshooting

Diagnoses failed, stuck, or silent Google Cloud Application Integration runs and Integration Connectors tasks using the REST API, Cloud Logging, and Cloud Monitoring. Use when an integration fails, returns HTTP 200 without doing the expected work, hangs in a suspended or retry state, or hits IAM, run-as service account, connector health, or quota errors. Do not use for initial region provisioning (use application-integration-basics) or building and deploying versions (use application-integration-authoring).

This plugin packages the [`application-integration-troubleshooting`](skills/application-integration-troubleshooting/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/application-integration-troubleshooting) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/application-integration-troubleshooting/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install application-integration-troubleshooting@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dapplication-integration-troubleshooting),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `application-integration-troubleshooting`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
