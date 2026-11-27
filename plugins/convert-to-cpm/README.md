# convert-to-cpm

Convert .NET projects and solutions (.sln, .slnx) to NuGet Central Package Management (CPM) using Directory.Packages.props. USE FOR: converting to CPM, centralizing or aligning NuGet package versions across multiple projects, inlining MSBuild version properties from Directory.Build.props into Directory.Packages.props, resolving version conflicts or mismatches across a solution or repository, updating or bumping or syncing package versions across projects. Also activate when packages are out of sync, drifting, or inconsistent -- even without the user mentioning CPM. Provides baseline build capture, version conflict resolution, build validation with binlog comparison, and a structured post-conversion report. DO NOT USE FOR: packages.config projects (must migrate to PackageReference first) or repositories that already have CPM fully enabled.

This plugin packages the [`convert-to-cpm`](skills/convert-to-cpm/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-nuget/skills/convert-to-cpm) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/convert-to-cpm/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install convert-to-cpm@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dconvert-to-cpm),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `convert-to-cpm`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
