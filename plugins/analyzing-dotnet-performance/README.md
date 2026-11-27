# analyzing-dotnet-performance

Scans .NET code for ~50 performance anti-patterns across async, memory, strings, collections, LINQ, regex, serialization, and I/O with tiered severity classification. Use when analyzing .NET code for optimization opportunities, reviewing hot paths, or auditing allocation-heavy patterns.

This plugin packages the [`analyzing-dotnet-performance`](skills/analyzing-dotnet-performance/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-diag/skills/analyzing-dotnet-performance) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/analyzing-dotnet-performance/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install analyzing-dotnet-performance@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Danalyzing-dotnet-performance),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `analyzing-dotnet-performance`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
