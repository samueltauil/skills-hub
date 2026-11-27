# create-datadriven-aspnetcore

Generate or scaffold ASP.NET Core code — Razor Pages, Blazor components, MVC controllers, views, and Minimal API endpoints — without using ASP.NET Core CLI scaffolding/code-generation tools. Use when (1) adding CRUD pages, views, or API endpoints backed by Entity Framework (EF Core) and a database, (2) generating code to create, read, update, and delete data using a DbContext, (3) scaffolding UI components that match the project's existing CSS framework and coding patterns, or (4) creating data-driven forms, tables, and navigation for a model class. Do not use for non-ASP.NET projects or when CLI-based scaffolding is preferred.

This plugin packages the [`create-datadriven-aspnetcore`](skills/create-datadriven-aspnetcore/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-data/skills/create-datadriven-aspnetcore) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/create-datadriven-aspnetcore/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install create-datadriven-aspnetcore@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcreate-datadriven-aspnetcore),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `create-datadriven-aspnetcore`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
