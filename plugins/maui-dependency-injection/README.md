# maui-dependency-injection

Guidance for configuring dependency injection in .NET MAUI apps — service registration in MauiProgram.cs, lifetime selection (Singleton / Transient / Scoped), constructor injection, Shell navigation auto-resolution, platform-specific registrations, and testability patterns. USE FOR: "dependency injection", "DI setup", "AddSingleton", "AddTransient", "AddScoped", "service registration", "constructor injection", "IServiceProvider", "MauiProgram DI", "register services", "BindingContext injection". DO NOT USE FOR: data binding (use maui-data-binding), Shell route configuration (use maui-shell-navigation), unit-test mocking frameworks (use standard xUnit and NSubstitute patterns).

This plugin packages the [`maui-dependency-injection`](skills/maui-dependency-injection/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-maui/skills/maui-dependency-injection) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/maui-dependency-injection/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install maui-dependency-injection@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmaui-dependency-injection),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `maui-dependency-injection`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
