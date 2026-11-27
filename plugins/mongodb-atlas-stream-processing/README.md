# mongodb-atlas-stream-processing

Manages MongoDB Atlas Stream Processing (ASP) workflows. Handles workspace provisioning, data source/sink connections, processor lifecycle operations, debugging diagnostics, and tier sizing. Supports Kafka, Atlas clusters, S3, Apache Iceberg (with Unity and Horizon catalogs), HTTPS, and Lambda integrations for streaming data workloads and event processing. NOT for general MongoDB queries or Atlas cluster management. Requires MongoDB MCP Server with Atlas API credentials.

This plugin packages the [`mongodb-atlas-stream-processing`](skills/mongodb-atlas-stream-processing/SKILL.md) skill from
[mongodb/agent-skills](https://github.com/mongodb/agent-skills/tree/main/skills/mongodb-atlas-stream-processing) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/mongodb-atlas-stream-processing/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install mongodb-atlas-stream-processing@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmongodb-atlas-stream-processing),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `mongodb-atlas-stream-processing`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[mongodb/agent-skills](https://github.com/mongodb/agent-skills).
