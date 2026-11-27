# mcp-builder

Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).

This plugin packages the [`mcp-builder`](skills/mcp-builder/SKILL.md) skill from
[anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/mcp-builder) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/mcp-builder/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install mcp-builder@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmcp-builder),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `mcp-builder`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[anthropics/skills](https://github.com/anthropics/skills).
