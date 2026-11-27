# template-authoring

Guides creation and validation of custom dotnet new templates from existing projects. Generates a .template.config/template.json that preserves the source project's conventions. USE FOR: creating a reusable dotnet new template from an existing project, bootstrapping .template.config/template.json with correct identity, shortName, parameters, and post-actions, adding parameters or conditional content to a template you are authoring, validating the template.json you are authoring before publishing, packaging templates as NuGet packages for distribution. DO NOT USE FOR: validating an existing template.json as a standalone task (use template-validation), finding or using existing templates (use template-discovery and template-instantiation), MSBuild project file issues unrelated to template authoring, NuGet package publishing (only template packaging structure).

This plugin packages the [`template-authoring`](skills/template-authoring/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-template-engine/skills/template-authoring) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/template-authoring/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install template-authoring@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dtemplate-authoring),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `template-authoring`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
