# property-patterns

Diagnose and fix concrete MSBuild property defects in projects and existing shared-file hierarchies. USE FOR: conditions, defaults, append versus overwrite, last-write-wins values, OS/TFM checks, portable paths, normalization, and reviews centered on those property defects. Property defects in Directory.Build.* remain in scope, including overwritten values across parent/child imports and conditions that run before TargetFramework is set, even when the fix changes import order or moves a property group to .targets. DO NOT USE FOR: placement-only or import-only requests with no concrete property defect, such as discovering shared files or choosing which file owns a target or customization (use directory-build-organization); item operations; target structure; broad reviews without a concrete property defect; non-MSBuild work.

This plugin packages the [`property-patterns`](skills/property-patterns/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-msbuild/skills/property-patterns) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/property-patterns/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install property-patterns@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dproperty-patterns),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `property-patterns`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
