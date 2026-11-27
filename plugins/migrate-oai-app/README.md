# migrate-oai-app

This skill should be used when the user asks to "migrate from OpenAI Apps SDK", "convert OpenAI App to MCP", "port from window.openai", "migrate from skybridge", "convert openai/outputTemplate", or needs guidance on converting OpenAI Apps SDK applications to MCP Apps SDK. Provides step-by-step migration guidance with API mapping tables.

This plugin packages the [`migrate-oai-app`](skills/migrate-oai-app/SKILL.md) skill from
[modelcontextprotocol/ext-apps](https://github.com/modelcontextprotocol/ext-apps/tree/main/plugins/mcp-apps/skills/migrate-oai-app) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/migrate-oai-app/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install migrate-oai-app@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmigrate-oai-app),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `migrate-oai-app`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[modelcontextprotocol/ext-apps](https://github.com/modelcontextprotocol/ext-apps).
