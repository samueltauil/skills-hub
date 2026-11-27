# dotnet-webapi

Guides creation and modification of ASP.NET Core Web API endpoints with correct HTTP semantics, OpenAPI metadata, and error handling. USE FOR: adding new API endpoints (controllers or minimal APIs), wiring up OpenAPI/Swagger, creating .http test files, setting up global error handling middleware. DO NOT USE FOR: general C# coding style, EF Core data access or query optimization (use optimizing-ef-core-queries), frontend/Blazor work, gRPC services, or SignalR hubs.

This plugin packages the [`dotnet-webapi`](skills/dotnet-webapi/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-aspnetcore/skills/dotnet-webapi) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/dotnet-webapi/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install dotnet-webapi@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddotnet-webapi),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `dotnet-webapi`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
