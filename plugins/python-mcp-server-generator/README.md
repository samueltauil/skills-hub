# python-mcp-server-generator

Use this skill when the user wants to create a new Model Context Protocol (MCP) server in Python. Also use it to expose Python functions, an API, or a database to AI clients as MCP tools. The skill makes a uv project with the MCP Python SDK v2 (MCPServer), typed tools, in-memory tests, and client configuration. Do not use it for an MCP client or for a server in another language.

This plugin packages the [`python-mcp-server-generator`](skills/python-mcp-server-generator/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/python-mcp-server-generator) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/python-mcp-server-generator/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install python-mcp-server-generator@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpython-mcp-server-generator),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `python-mcp-server-generator`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
