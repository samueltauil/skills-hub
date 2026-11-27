# expo-dev-client

Build and distribute Expo development clients locally or via TestFlight for internal testing. For production TestFlight releases and store submission, use the eas-app-stores skill.

This plugin packages the [`expo-dev-client`](skills/expo-dev-client/SKILL.md) skill from
[expo/skills](https://github.com/expo/skills/tree/main/plugins/expo/skills/expo-dev-client) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/expo-dev-client/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install expo-dev-client@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dexpo-dev-client),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `expo-dev-client`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[expo/skills](https://github.com/expo/skills).
