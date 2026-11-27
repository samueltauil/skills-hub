# csharp-scripts

Run file-based C# apps with the .NET CLI when the user explicitly wants C#/.NET code without creating a project. Use for C# language/API experiments, one-file C# apps, small multi-file C# apps composed with `#:include`/`#:exclude`, or C# file-based apps linked with `#:ref`. Do not use for language-agnostic throwaway scripts, generic computations, Python/PowerShell-style automation, full projects, or existing app integration.

This plugin packages the [`csharp-scripts`](skills/csharp-scripts/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-advanced/skills/csharp-scripts) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/csharp-scripts/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install csharp-scripts@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcsharp-scripts),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `csharp-scripts`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
