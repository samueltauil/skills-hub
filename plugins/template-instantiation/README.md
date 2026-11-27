# template-instantiation

Creates .NET projects from templates with validated parameters, smart defaults, Central Package Management adaptation, and latest NuGet version resolution. USE FOR: creating new dotnet projects, scaffolding solutions with multiple projects, installing or uninstalling template packages, creating projects that respect Directory.Packages.props (CPM), composing multi-project solutions (API + tests + library), getting latest NuGet package versions in newly created projects. DO NOT USE FOR: finding templates (use template-discovery), producing a detailed side-by-side comparison of templates (use template-comparison), authoring custom templates (use template-authoring), deciding cross-parameter defaults such as which framework to pair with native AOT or whether to keep HTTPS when auth is enabled (use template-smart-defaults), modifying existing projects or adding NuGet packages to existing projects.

This plugin packages the [`template-instantiation`](skills/template-instantiation/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-template-engine/skills/template-instantiation) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/template-instantiation/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install template-instantiation@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dtemplate-instantiation),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `template-instantiation`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
