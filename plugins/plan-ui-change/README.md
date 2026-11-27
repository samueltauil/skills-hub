# plan-ui-change

Plan complex Blazor UI features by decomposing them into focused components. USE FOR: building a complex Blazor page with multiple sections, planning component decomposition, designing a multi-section dashboard or layout, breaking down a large UI feature into composable components, pages with sidebars and content panels, any page with 3+ distinct visual sections or multiple interacting sub-features, identifying parent-child relationships and data flow. DO NOT USE FOR: creating new Blazor projects or apps from scratch (use create-blazor-project), implementing a single individual component (use author-component), writing component code with parameters and EventCallback (use author-component), or simple single-component pages.

This plugin packages the [`plan-ui-change`](skills/plan-ui-change/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-blazor/skills/plan-ui-change) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/plan-ui-change/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install plan-ui-change@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dplan-ui-change),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `plan-ui-change`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
