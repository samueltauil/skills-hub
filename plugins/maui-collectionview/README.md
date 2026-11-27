# maui-collectionview

Guidance for implementing CollectionView in .NET MAUI apps — data display, layouts (list & grid), selection, grouping, scrolling, empty views, templates, incremental loading, swipe actions, and pull-to-refresh. USE FOR: "CollectionView", "list view", "grid layout", "data template", "item template", "grouping", "pull to refresh", "incremental loading", "swipe actions", "empty view", "selection mode", "scroll to item", displaying scrollable data, replacing ListView. DO NOT USE FOR: simple static layouts without scrollable data (use Grid or StackLayout), map pin lists (use Microsoft.Maui.Controls.Maps), table-based data entry forms, non-MAUI list controls, CarouselView or BindableLayout questions, platform-specific handler or renderer customization, diagnosing CollectionView bugs in the MAUI framework itself, or general MVVM/binding questions that merely happen to mention a list (use maui-data-binding).

This plugin packages the [`maui-collectionview`](skills/maui-collectionview/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-maui/skills/maui-collectionview) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/maui-collectionview/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install maui-collectionview@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmaui-collectionview),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `maui-collectionview`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
