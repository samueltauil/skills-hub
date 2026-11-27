# msbuild-antipatterns

DO NOT INVOKE when the primary request explicitly asks to convert, migrate, modernize, or rewrite a legacy/old-style project to SDK style; use msbuild-modernization. Migration prompts often mention ToolsVersion, explicit Compile/Reference entries, packages.config, or Microsoft.CSharp.targets, but merely reviewing or auditing a file that contains those patterns remains in scope here. USE FOR broad review, audit, lint, or maintainability/correctness checks of project/build files, including custom targets; prioritized cross-cutting findings; discrete anti-patterns; F# ordering/FS0039; cross-platform paths; and focused Import safety verdicts. Review/audit is analysis-only unless fixes are requested. For concrete property/item defects use property-patterns/item-management; use target-authoring for implementation and extension-points for NuGet auto-import/layout discovery. Exclude non-MSBuild systems.

This plugin packages the [`msbuild-antipatterns`](skills/msbuild-antipatterns/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-msbuild/skills/msbuild-antipatterns) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/msbuild-antipatterns/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install msbuild-antipatterns@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmsbuild-antipatterns),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `msbuild-antipatterns`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
