# add-app-to-server

This skill should be used when the user asks to "add an app to my MCP server", "add UI to my MCP server", "add a view to my MCP tool", "enrich MCP tools with UI", "add interactive UI to existing server", "add MCP Apps to my server", or needs to add interactive UI capabilities to an existing MCP server that already has tools. Provides guidance for analyzing existing tools and adding MCP Apps UI resources.

This plugin packages the [`add-app-to-server`](skills/add-app-to-server/SKILL.md) skill from
[modelcontextprotocol/ext-apps](https://github.com/modelcontextprotocol/ext-apps/tree/main/plugins/mcp-apps/skills/add-app-to-server) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/add-app-to-server/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install add-app-to-server@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dadd-app-to-server),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `add-app-to-server`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[modelcontextprotocol/ext-apps](https://github.com/modelcontextprotocol/ext-apps).
