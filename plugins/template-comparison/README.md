# template-comparison

Compares two or more dotnet new templates side by side to help users choose between them based on parameters, feature support, frameworks, and classifications. USE FOR: deciding between similar templates (webapi vs webapp, blazor vs blazorwasm, console vs worker), producing a side-by-side comparison of parameters and feature support, understanding how templates differ before creating a project. DO NOT USE FOR: creating a project from a template (use template-instantiation), authoring or validating custom templates (use template-authoring and template-validation), general single-template discovery (use template-discovery).

This plugin packages the [`template-comparison`](skills/template-comparison/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-template-engine/skills/template-comparison) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/template-comparison/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install template-comparison@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dtemplate-comparison),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `template-comparison`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
