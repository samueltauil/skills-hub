# expo-web-to-native

Migrate an existing web React app to a native iOS/Android app with Expo. Use when the user wants to turn a website into a mobile app, port a Next.js/Vite/CRA React codebase to React Native, reuse web code on native incrementally, or asks how web idioms (the DOM, CSS, React Router, localStorage, window) map to native. This is the end-to-end migration guide; use the `expo-dom` skill for the DOM-component mechanism itself.

This plugin packages the [`expo-web-to-native`](skills/expo-web-to-native/SKILL.md) skill from
[expo/skills](https://github.com/expo/skills/tree/main/plugins/expo/skills/expo-web-to-native) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/expo-web-to-native/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install expo-web-to-native@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dexpo-web-to-native),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `expo-web-to-native`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[expo/skills](https://github.com/expo/skills).
