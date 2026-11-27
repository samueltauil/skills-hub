# mvvm-toolkit-di

Wire CommunityToolkit.Mvvm ViewModels into Microsoft.Extensions.DependencyInjection. Covers the .NET Generic Host composition root, constructor injection, service lifetimes (Singleton / Transient / Scoped), IMessenger registration, resolving ViewModels in Views, keyed services, testing seams, and the legacy Ioc.Default escape hatch. Use across WPF, WinUI 3, .NET MAUI, Uno, and Avalonia.

This plugin packages the [`mvvm-toolkit-di`](skills/mvvm-toolkit-di/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/mvvm-toolkit-di) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/mvvm-toolkit-di/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install mvvm-toolkit-di@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmvvm-toolkit-di),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `mvvm-toolkit-di`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
