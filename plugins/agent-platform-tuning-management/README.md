# agent-platform-tuning-management

Manages GenAI tuning jobs in Agent Platform. Use this to list, get, or cancel ongoing model tuning jobs. Don't use for fine-tuning models (use `agent-platform-tuning`), deploying models to endpoints (use `agent-platform-deploy`), or managing serving endpoints (use `agent-platform-endpoint-management`).

This plugin packages the [`agent-platform-tuning-management`](skills/agent-platform-tuning-management/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/agent-platform-tuning-management) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/agent-platform-tuning-management/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install agent-platform-tuning-management@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dagent-platform-tuning-management),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `agent-platform-tuning-management`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
