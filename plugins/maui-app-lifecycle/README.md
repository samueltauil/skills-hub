# maui-app-lifecycle

.NET MAUI app lifecycle guidance — the four app states, cross-platform Window lifecycle events (Created, Activated, Deactivated, Stopped, Resumed, Destroying), platform-specific lifecycle mapping, backgrounding and resume behavior, and state-preservation patterns. USE FOR: "app lifecycle", "window lifecycle events", "save state on background", "resume app", "OnStopped", "OnResumed", "backgrounding", "deactivated event", "ConfigureLifecycleEvents", "platform lifecycle hooks". DO NOT USE FOR: navigation events (use maui-shell-navigation), dependency injection setup (use maui-dependency-injection), platform API invocation (use conditional compilation and partial classes).

This plugin packages the [`maui-app-lifecycle`](skills/maui-app-lifecycle/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-maui/skills/maui-app-lifecycle) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/maui-app-lifecycle/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install maui-app-lifecycle@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmaui-app-lifecycle),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `maui-app-lifecycle`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
