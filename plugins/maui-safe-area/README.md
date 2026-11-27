# maui-safe-area

.NET MAUI safe area and edge-to-edge layout guidance for .NET 10+. Covers the new SafeAreaEdges property, SafeAreaRegions enum, per-edge control, keyboard avoidance, Blazor Hybrid CSS safe areas, migration from legacy iOS-only APIs, and platform-specific behavior for Android, iOS, and Mac Catalyst. USE FOR: "safe area", "edge-to-edge", "SafeAreaEdges", "SafeAreaRegions", "keyboard avoidance", "notch insets", "status bar overlap", "iOS safe area", "Android edge-to-edge", "content behind status bar", "UseSafeArea migration", "soft input keyboard", "IgnoreSafeArea replacement". DO NOT USE FOR: general layout or grid design (use Grid and StackLayout), app lifecycle handling (use maui-app-lifecycle), theming or styling (use maui-theming), or Shell navigation structure.

This plugin packages the [`maui-safe-area`](skills/maui-safe-area/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-maui/skills/maui-safe-area) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/maui-safe-area/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install maui-safe-area@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmaui-safe-area),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `maui-safe-area`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
