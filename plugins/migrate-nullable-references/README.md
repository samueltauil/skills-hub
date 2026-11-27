# migrate-nullable-references

Enable nullable reference types in a C# project and systematically resolve all warnings. USE FOR: adopting NRTs in existing codebases, file-by-file or project-wide migration, fixing CS8602/CS8618/CS86xx warnings, annotating APIs for nullability, cleaning up null-forgiving operators, upgrading dependencies with new nullable annotations. DO NOT USE FOR: projects already fully migrated with zero warnings (unless auditing suppressions), fixing a handful of nullable warnings in code that already has NRTs enabled, suppressing warnings without fixing them, C# 7.3 or earlier projects. INVOKES: Get-NullableReadiness.ps1 scanner script.

This plugin packages the [`migrate-nullable-references`](skills/migrate-nullable-references/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-upgrade/skills/migrate-nullable-references) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/migrate-nullable-references/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install migrate-nullable-references@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmigrate-nullable-references),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `migrate-nullable-references`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
