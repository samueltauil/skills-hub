# binlog-failure-analysis

Analyze MSBuild binary logs to diagnose build failures. USE FOR: build errors that are unclear from console output, diagnosing cascading failures across multi-project builds, tracing MSBuild target execution order, and generally any MSBuild build issues. Requires an existing .binlog file. DO NOT USE FOR: generating binlogs (use binlog-generation), binlog MCP startup or connection failures (use troubleshoot-binlog-mcp), non-MSBuild build systems.

This plugin packages the [`binlog-failure-analysis`](skills/binlog-failure-analysis/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-msbuild/skills/binlog-failure-analysis) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/binlog-failure-analysis/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install binlog-failure-analysis@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dbinlog-failure-analysis),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `binlog-failure-analysis`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
