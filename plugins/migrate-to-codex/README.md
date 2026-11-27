# migrate-to-codex

Migrate supported instruction files, skills, agents, and MCP config into Codex project and global files.

This plugin packages the [`migrate-to-codex`](skills/migrate-to-codex/SKILL.md) skill from
[openai/skills](https://github.com/openai/skills/tree/main/skills/.curated/migrate-to-codex) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/migrate-to-codex/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install migrate-to-codex@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmigrate-to-codex),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `migrate-to-codex`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[openai/skills](https://github.com/openai/skills).
