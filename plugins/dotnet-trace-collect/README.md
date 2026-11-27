# dotnet-trace-collect

Guide developers through capturing diagnostic artifacts to diagnose production .NET performance issues. Use when the user needs help choosing diagnostic tools, collecting performance data, or understanding tool trade-offs across different environments (Windows/Linux, .NET Framework/modern .NET, container/non-container).

This plugin packages the [`dotnet-trace-collect`](skills/dotnet-trace-collect/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-diag/skills/dotnet-trace-collect) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/dotnet-trace-collect/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install dotnet-trace-collect@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddotnet-trace-collect),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `dotnet-trace-collect`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
