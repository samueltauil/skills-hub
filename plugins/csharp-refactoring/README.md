# csharp-refactoring

Safely refactors C#/.NET code without changing behavior. USE FOR any request to refactor, rename, move, extract, inline, merge, consolidate, deduplicate, split, or modernize C# code, even a small extract, inline, or rename, or merging near-identical types; green builds miss drift in #if branches, generated partials, and reflection/config names. When a changed member is visible outside the assembly (PublicAPI.*.txt, InternalsVisibleTo, shipped package), also invoke dotnet-breaking-changes; local/private renames do not need it. Also use when a request calls a feature, bug fix, package/framework upgrade, or public nullability change a refactor and the behavior-changing part must be separated or declined. DO NOT USE FOR ordinary feature or bug fixes not presented as refactoring; standalone upgrades after reclassification (use dotnet-upgrade); adding tests; or formatting-only work.

This plugin packages the [`csharp-refactoring`](skills/csharp-refactoring/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet/skills/csharp-refactoring) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/csharp-refactoring/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install csharp-refactoring@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcsharp-refactoring),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `csharp-refactoring`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
