# migrate-dotnet9-to-dotnet10

Migrate a .NET 9 project or solution to .NET 10 and resolve all breaking changes. USE FOR: upgrading TargetFramework from net9.0 to net10.0, fixing build errors after updating the .NET 10 SDK, resolving source and behavioral changes in .NET 10 / C# 14 / ASP.NET Core 10 / EF Core 10, updating Dockerfiles for Debian-to-Ubuntu base images, resolving obsoletion warnings (SYSLIB0058-SYSLIB0062), adapting to SDK/NuGet changes (NU1510, PrunePackageReference), migrating System.Linq.Async to built-in AsyncEnumerable, fixing OpenApi v2 API changes, cryptography renames, and C# 14 compiler changes (field keyword, extension keyword, span overloads). DO NOT USE FOR: .NET Framework migrations, upgrading from .NET 8 or earlier (use migrate-dotnet8-to-dotnet9 first), greenfield .NET 10 projects, or cosmetic modernization. LOADS REFERENCES: csharp-compiler, core-libraries, sdk-msbuild (always); aspnet-core, efcore, cryptography, extensions-hosting, serialization-networking, winforms-wpf, containers-interop (selective).

This plugin packages the [`migrate-dotnet9-to-dotnet10`](skills/migrate-dotnet9-to-dotnet10/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-upgrade/skills/migrate-dotnet9-to-dotnet10) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/migrate-dotnet9-to-dotnet10/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install migrate-dotnet9-to-dotnet10@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmigrate-dotnet9-to-dotnet10),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `migrate-dotnet9-to-dotnet10`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
