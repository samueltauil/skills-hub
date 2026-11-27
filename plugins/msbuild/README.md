# msbuild

Use before MSBuild custom-target or incremental-generation repairs, XML/import/hook review, .binlog capture/replay, or assessing supported/unsupported build-speedup claims and controlled timings, even without a checkout. For MSBuild authoring itself, activate before reviewing/editing .proj/.props/.targets/.csproj/.fsproj/.vbproj or Directory.Build files, including no-change import reviews. Framework/API/.NET/ASP.NET upgrade plans and working non-SDK-to-SDK/packages.config conversions are migrations, even if they mention .csproj/NuGet: DO NOT activate. A failing assertion after a successful build is code/test debugging: DO NOT activate. Check Import/Exists, required and NuGet build/buildTransitive/nuspec imports, conditions, Inputs/Outputs, stale outputs and incorrect skips. Build checks use copies; source inputs stay read-only. Diagnose failed dotnet build/restore/pack/publish or slow evaluation/compilation/copying. Exclude SDK installation alone, C# refactoring, runtime CPU profiling and non-MSBuild builds.

This plugin packages the [`msbuild`](skills/msbuild/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet/skills/msbuild) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/msbuild/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install msbuild@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmsbuild),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `msbuild`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
