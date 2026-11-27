# collect-user-input

Build forms, validate data, and react to user input in Blazor. USE FOR adding forms, search boxes, filter panels, inline editing, data-entry UI, file uploads, validation (annotations or custom), handling form submissions, and binding input controls. Covers EditForm, built-in input components, DataAnnotationsValidator, custom validation, SSR form patterns (SupplyParameterFromForm, FormName, AntiforgeryToken, Enhance), and @bind for simple interactive controls. DO NOT USE for project scaffolding (see create-blazor-project) or prerendering issues (see support-prerendering).

This plugin packages the [`collect-user-input`](skills/collect-user-input/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-blazor/skills/collect-user-input) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/collect-user-input/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install collect-user-input@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcollect-user-input),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `collect-user-input`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
