# create-mcp-app

This skill should be used when the user asks to "create an MCP App", "add a UI to an MCP tool", "build an interactive MCP View", "scaffold an MCP App", or needs guidance on MCP Apps SDK patterns, UI-resource registration, MCP App lifecycle, or host integration. Provides comprehensive guidance for building MCP Apps with interactive UIs.

This plugin packages the [`create-mcp-app`](skills/create-mcp-app/SKILL.md) skill from
[modelcontextprotocol/ext-apps](https://github.com/modelcontextprotocol/ext-apps/tree/main/plugins/mcp-apps/skills/create-mcp-app) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/create-mcp-app/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install create-mcp-app@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcreate-mcp-app),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `create-mcp-app`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[modelcontextprotocol/ext-apps](https://github.com/modelcontextprotocol/ext-apps).
