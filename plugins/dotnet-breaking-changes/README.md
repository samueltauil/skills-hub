# dotnet-breaking-changes

Use before changing .NET/C# code whose callers you do not control: a NuGet library, or a repo with PublicAPI.Shipped/Unshipped.txt, ApiCompat, multiple TargetFrameworks, InternalsVisibleTo, or generated (.g.cs) partials. Green builds miss silent breaks from optional parameters, parameter names, sealing, const values, nullability, and #if. USE FOR: "without breaking existing callers"; adding a public method, overload, optional parameter, or interface member to a shipped library; renaming a public method or an internal helper a friend assembly uses; consolidating duplicated logic; changing a signature, nullability, default, or attribute; adding a target framework; RS0016/RS0017 or ApiCompat errors; "is this PR breaking?". For a rename, extract, or merge, also invoke csharp-refactoring. DO NOT USE FOR: an executable whose callers all live in one project; renaming a local variable or private member, even in a shipped library; formatting; framework/SDK/NuGet upgrades (use dotnet-upgrade).

This plugin packages the [`dotnet-breaking-changes`](skills/dotnet-breaking-changes/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet/skills/dotnet-breaking-changes) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/dotnet-breaking-changes/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install dotnet-breaking-changes@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddotnet-breaking-changes),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `dotnet-breaking-changes`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
