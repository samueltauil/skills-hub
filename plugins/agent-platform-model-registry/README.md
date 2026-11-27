# agent-platform-model-registry

Agent Platform Model Registry Management. Use when you need to upload, list, describe, update, or delete machine learning models (and their versions) in the Agent Platform Model Registry. Don't use for model training, model deployment to endpoints, or managing non-Agent Platform models.

This plugin packages the [`agent-platform-model-registry`](skills/agent-platform-model-registry/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/agent-platform-model-registry) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/agent-platform-model-registry/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install agent-platform-model-registry@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dagent-platform-model-registry),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `agent-platform-model-registry`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
