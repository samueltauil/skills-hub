# directory-build-organization

USE ONLY for (1) two or more projects with repeated MSBuild policy, targets, or package versions, or (2) an existing Directory.Build.props/targets/rsp hierarchy with an import, placement, or layering defect. A one-project repo without an existing Directory.Build file is outside scope; do not load this skill. Covers centralizing shared policy and targets, Directory.Packages.props across projects, parent hierarchy/import structure, props-versus-targets placement, and folder/project exceptions. An existing hierarchy defect remains in scope when only one project is affected. For property value or condition semantics use property-patterns. Exclude legacy-to-SDK migration and non-MSBuild systems.

This plugin packages the [`directory-build-organization`](skills/directory-build-organization/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-msbuild/skills/directory-build-organization) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/directory-build-organization/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install directory-build-organization@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddirectory-build-organization),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `directory-build-organization`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
