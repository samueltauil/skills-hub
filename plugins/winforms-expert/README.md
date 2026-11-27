# winforms-expert

Create, modify, debug, or review Windows Forms applications only when the request contains a concrete Windows Forms marker. USE FOR: WinForms, Windows Forms, System.Windows.Forms, WinForms Form or UserControl designer files (*.Designer.cs or *.Designer.vb), Visual Studio WinForms Designer, TableLayoutPanel, BindingSource, DataGridView, Control.InvokeAsync, component-tray ownership, or custom control serialization. DO NOT USE FOR: WPF or WPF XAML, including Window.InputBindings, KeyBinding, commands, or DataContext; .NET MAUI; Avalonia; or any request where none of the listed Windows Forms markers is present.

This plugin packages the [`winforms-expert`](skills/winforms-expert/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-winforms/skills/winforms-expert) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/winforms-expert/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install winforms-expert@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dwinforms-expert),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `winforms-expert`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
