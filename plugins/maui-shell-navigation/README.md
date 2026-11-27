# maui-shell-navigation

Guide for implementing Shell-based navigation in .NET MAUI apps. Covers AppShell setup, visual hierarchy (FlyoutItem, TabBar, Tab, ShellContent), URI-based navigation with GoToAsync, route registration, query parameters, back navigation, flyout and tab configuration, navigation events, and navigation guards. Use when: setting up Shell navigation, adding tabs or flyout menus, navigating between pages with GoToAsync, passing parameters between pages, registering routes, customizing back button behavior, or guarding navigation with confirmation dialogs. Do not use for: deep linking from external URLs (see .NET MAUI deep linking documentation), data binding on pages (use maui-data-binding), dependency injection setup (use maui-dependency-injection), or NavigationPage-only apps that don't use Shell.

This plugin packages the [`maui-shell-navigation`](skills/maui-shell-navigation/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-maui/skills/maui-shell-navigation) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/maui-shell-navigation/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install maui-shell-navigation@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmaui-shell-navigation),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `maui-shell-navigation`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
