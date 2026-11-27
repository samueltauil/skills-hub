# migrate-dotnet10-to-dotnet11

Migrate a .NET 10 project or solution to .NET 11 and resolve all breaking changes. This is a MIGRATION skill — use it when upgrading from .NET 10 to .NET 11, NOT for writing new programs. USE FOR: upgrading TargetFramework from net10.0 to net11.0, fixing build errors after updating the .NET 11 SDK, resolving source-breaking and behavioral changes in .NET 11 runtime, C# 15 compiler, and EF Core 11, adapting to updated minimum hardware requirements (x86-64-v2, Arm64 LSE), and updating CI/CD pipelines and Dockerfiles for .NET 11. DO NOT USE FOR: .NET Framework migrations, upgrading from .NET 9 or earlier, greenfield .NET 11 projects, or cosmetic modernization unrelated to the upgrade. NOTE: .NET 11 is in preview. Covers breaking changes through Preview 3.

This plugin packages the [`migrate-dotnet10-to-dotnet11`](skills/migrate-dotnet10-to-dotnet11/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-upgrade/skills/migrate-dotnet10-to-dotnet11) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/migrate-dotnet10-to-dotnet11/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install migrate-dotnet10-to-dotnet11@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmigrate-dotnet10-to-dotnet11),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `migrate-dotnet10-to-dotnet11`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
