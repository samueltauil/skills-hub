# convert-blazor-server-to-webapp

Guides conversion of a pre-.NET 8 Blazor Server app into a .NET 8+ Blazor Web App. USE FOR: migrating apps that use AddServerSideBlazor and MapBlazorHub to the AddRazorComponents/MapRazorComponents model, converting _Host.cshtml to an App.razor root component, replacing blazor.server.js with blazor.web.js, migrating CascadingAuthenticationState to a service, adopting new Blazor Web App features like enhanced navigation and streaming rendering. DO NOT USE FOR: apps that are already Blazor Web Apps (already use AddRazorComponents and MapRazorComponents), Blazor WebAssembly or hosted Blazor WebAssembly apps (different migration path), apps that should stay on the Blazor Server hosting model without converting, or apps still targeting .NET Framework.

This plugin packages the [`convert-blazor-server-to-webapp`](skills/convert-blazor-server-to-webapp/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-aspnetcore/skills/convert-blazor-server-to-webapp) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/convert-blazor-server-to-webapp/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install convert-blazor-server-to-webapp@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dconvert-blazor-server-to-webapp),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `convert-blazor-server-to-webapp`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
