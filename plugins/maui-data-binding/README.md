# maui-data-binding

Guidance for .NET MAUI XAML and C# data bindings — compiled bindings, INotifyPropertyChanged / ObservableObject, value converters, binding modes, multi-binding, relative bindings, fallbacks, and MVVM best practices. USE FOR: setting up compiled bindings with x:DataType, implementing INotifyPropertyChanged or CommunityToolkit ObservableObject, creating IValueConverter / IMultiValueConverter, choosing binding modes, configuring BindingContext, relative bindings, binding fallbacks, StringFormat, code-behind SetBinding with lambdas, and enforcing XC0022/XC0025 warnings. DO NOT USE FOR: CollectionView item templates and layouts (use maui-collectionview), Shell navigation data passing (use maui-shell-navigation), dependency injection (use maui-dependency-injection), or animations triggered by property changes (use .NET MAUI animation APIs).

This plugin packages the [`maui-data-binding`](skills/maui-data-binding/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-maui/skills/maui-data-binding) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/maui-data-binding/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install maui-data-binding@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmaui-data-binding),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `maui-data-binding`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
