# migrate-dotnet8-to-dotnet9

Migrate a .NET 8 project to .NET 9 and resolve all breaking changes. USE FOR: upgrading TargetFramework from net8.0 to net9.0, fixing build errors after updating the .NET 9 SDK, resolving behavioral changes in .NET 9 / C# 13 / ASP.NET Core 9 / EF Core 9, replacing BinaryFormatter (now always throws), resolving SYSLIB0054-SYSLIB0057, adapting to params span overload resolution, fixing C# 13 compiler changes, updating HttpClientFactory for SocketsHttpHandler, and resolving EF Core 9 migration/Cosmos DB changes. DO NOT USE FOR: .NET Framework migrations, upgrading from .NET 7 or earlier, greenfield .NET 9 projects, or cosmetic modernization unrelated to the upgrade.

This plugin packages the [`migrate-dotnet8-to-dotnet9`](skills/migrate-dotnet8-to-dotnet9/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-upgrade/skills/migrate-dotnet8-to-dotnet9) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/migrate-dotnet8-to-dotnet9/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install migrate-dotnet8-to-dotnet9@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmigrate-dotnet8-to-dotnet9),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `migrate-dotnet8-to-dotnet9`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
