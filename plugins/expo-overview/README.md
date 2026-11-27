# expo-overview

Entry point for Expo and EAS tasks. Load first when the request mentions Expo, EAS, Expo Go, or an expo-* package, or the project has an expo dependency. Identify the goal, apply shared SDK and setup rules, and select the relevant skill. Includes fully specified tasks; excludes React Native projects without Expo or EAS signals.

This plugin packages the [`expo-overview`](skills/expo-overview/SKILL.md) skill from
[expo/skills](https://github.com/expo/skills/tree/main/plugins/expo/skills/expo-overview) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/expo-overview/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install expo-overview@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dexpo-overview),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `expo-overview`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[expo/skills](https://github.com/expo/skills).
