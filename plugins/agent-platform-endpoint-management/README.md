# agent-platform-endpoint-management

Manages Agent Platform serving endpoints. Use when you need to create, list, describe, update, or delete serving endpoints for model deployment on Agent Platform. Also use when troubleshooting endpoint permission, quota, or resource busy errors. Don't use for deploying models to endpoints or for running model evaluations.

This plugin packages the [`agent-platform-endpoint-management`](skills/agent-platform-endpoint-management/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/agent-platform-endpoint-management) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/agent-platform-endpoint-management/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install agent-platform-endpoint-management@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dagent-platform-endpoint-management),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `agent-platform-endpoint-management`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
