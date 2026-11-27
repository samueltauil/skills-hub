# agent-platform-prompt-management

Manages and orchestrates prompts in Agent Platform. Use when you need to create, list, retrieve, version, or delete managed prompts in Agent Platform. Don't use for model training, model deployment to endpoints, or managing non-Agent Platform prompts.

This plugin packages the [`agent-platform-prompt-management`](skills/agent-platform-prompt-management/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/agent-platform-prompt-management) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/agent-platform-prompt-management/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install agent-platform-prompt-management@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dagent-platform-prompt-management),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `agent-platform-prompt-management`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
