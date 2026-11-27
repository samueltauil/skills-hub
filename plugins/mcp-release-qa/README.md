# mcp-release-qa

Verify an MCP server before release by exercising a real protocol session, comparing runtime capabilities with source and documentation, testing failure paths, and recording reproducible evidence. Use when shipping or reviewing an MCP server, tool, resource, prompt, catalog, or install path.

This plugin packages the [`mcp-release-qa`](skills/mcp-release-qa/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/mcp-release-qa) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/mcp-release-qa/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install mcp-release-qa@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmcp-release-qa),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `mcp-release-qa`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
