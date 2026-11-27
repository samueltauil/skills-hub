# gemini-interactions-api

Guides the usage of Gemini Interactions API on Gemini Enterprise Agent Platform. Use when the user wants to use the stateful, server-managed Interactions API for multi-turn conversations, background execution, streaming, structured output, and function calling on the Agent Platform.

This plugin packages the [`gemini-interactions-api`](skills/gemini-interactions-api/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gemini-interactions-api) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gemini-interactions-api/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gemini-interactions-api@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgemini-interactions-api),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gemini-interactions-api`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
