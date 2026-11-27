# dotnet-mcp-builder

Build Model Context Protocol (MCP) servers in C#/.NET against the current ModelContextProtocol 2.x NuGet packages. Helps with cases the model gets wrong without guidance — stale versions (0.x preview or 1.x-era defaults), the v2 stateless-by-default HTTP flip, the 2026-07-28 spec deprecations (roots/sampling/logging), MCP Apps and Tasks extension packages, elicitation URL mode, per-session HTTP wiring, OAuth and reverse-proxy deploy specifics, and debugging MapMcp / STDIO / Streamable-HTTP errors. Also covers STDIO and Streamable HTTP transports (SSE is deprecated), tools, prompts, resources, completions, and a basic .NET MCP client. Trigger when the user says or implies any .NET MCP server work: ModelContextProtocol, McpServerTool, MapMcp, WithStdioServerTransport, "MCP server in C#", "MCP tool in dotnet", "expose this as MCP", or names a primitive (prompt/resource/elicitation/MCP App) in a .NET context. Skip for MCP work in other languages.

This plugin packages the [`dotnet-mcp-builder`](skills/dotnet-mcp-builder/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/dotnet-mcp-builder) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/dotnet-mcp-builder/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install dotnet-mcp-builder@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddotnet-mcp-builder),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `dotnet-mcp-builder`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
