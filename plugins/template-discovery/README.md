# template-discovery

Helps find, inspect, and compare (at a high level) .NET project templates. Resolves natural-language project descriptions to ranked template matches with pre-filled parameters. USE FOR: finding the right dotnet new template for a task, inspecting a template's parameters and constraints, understanding what a template produces before creating a project, resolving intent like "web API with auth" to concrete template + parameters. DO NOT USE FOR: actually creating projects (use template-instantiation), authoring custom templates (use template-authoring), producing a detailed side-by-side comparison (use template-comparison), choosing cross-parameter defaults during creation (use template-smart-defaults), MSBuild or build issues (use dotnet-msbuild plugin), NuGet package management unrelated to template packages.

This plugin packages the [`template-discovery`](skills/template-discovery/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-template-engine/skills/template-discovery) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/template-discovery/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install template-discovery@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dtemplate-discovery),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `template-discovery`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
