# csharp-expert

Route C# and .NET requests to the exact installed specialist or smallest dotnet/skills marketplace plugin. USE FOR: "which specialist should own this" or "how do I add the skill" requests involving ASP.NET Core endpoints, Blazor, MAUI binding, Windows Forms specialist selection or installation, EF Core queries, test framework migration (NUnit, xUnit, MSTest), framework migration, runtime CPU/allocation evidence, file-based C#, editor/compiler defects, a surviving MSBuild `.binlog`, or a plugin missing from `/skills`; also use for C# semantics when no narrower specialist exists, including "do I need another specialist?" questions. DO NOT USE FOR: requests that already name the exact installed specialist to invoke, or work unrelated to C# or .NET.

This plugin packages the [`csharp-expert`](skills/csharp-expert/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet/skills/csharp-expert) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/csharp-expert/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install csharp-expert@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcsharp-expert),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `csharp-expert`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
