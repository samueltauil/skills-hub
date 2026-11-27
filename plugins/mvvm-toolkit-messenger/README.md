# mvvm-toolkit-messenger

CommunityToolkit.Mvvm Messenger pub/sub for decoupled communication between ViewModels (or any objects). Covers WeakReferenceMessenger vs StrongReferenceMessenger, IRecipient<TMessage>, RequestMessage<T> / AsyncRequestMessage<T> / CollectionRequestMessage<T>, ValueChangedMessage<T>, channels (tokens), and the ObservableRecipient activation lifecycle. Use across WPF, WinUI 3, .NET MAUI, Uno, and Avalonia.

This plugin packages the [`mvvm-toolkit-messenger`](skills/mvvm-toolkit-messenger/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/mvvm-toolkit-messenger) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/mvvm-toolkit-messenger/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install mvvm-toolkit-messenger@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmvvm-toolkit-messenger),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `mvvm-toolkit-messenger`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
