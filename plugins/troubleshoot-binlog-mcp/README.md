# troubleshoot-binlog-mcp

Diagnose dotnet-msbuild binlog MCP startup failures. USE FOR: CONNECTION_CLOSED, binlog server won't connect, missing binlog tools, Microsoft.AITools.BinlogMcp not found, dnx launch errors. Checks workspace SDK, feeds, and source mapping without bypassing policy. DO NOT USE FOR: errors inside a binlog (use binlog-failure-analysis), capturing binlogs (use binlog-generation), unrelated MCP servers.

This plugin packages the [`troubleshoot-binlog-mcp`](skills/troubleshoot-binlog-mcp/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-msbuild/skills/troubleshoot-binlog-mcp) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/troubleshoot-binlog-mcp/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install troubleshoot-binlog-mcp@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dtroubleshoot-binlog-mcp),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `troubleshoot-binlog-mcp`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
