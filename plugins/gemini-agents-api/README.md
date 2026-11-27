# gemini-agents-api

Manages custom Agent resources on Gemini Enterprise Agent Platform. Use when the user wants to programmatically create, configure, list, update, or delete stateful, server-managed Agent resources (including mounting files, skills, and tools) before executing conversations.

This plugin packages the [`gemini-agents-api`](skills/gemini-agents-api/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gemini-agents-api) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gemini-agents-api/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gemini-agents-api@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgemini-agents-api),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gemini-agents-api`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
