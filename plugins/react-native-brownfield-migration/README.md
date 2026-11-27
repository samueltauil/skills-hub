# react-native-brownfield-migration

Implements an accepted incremental brownfield migration from native iOS or Android to React Native or Expo using @callstack/react-native-brownfield. Use after the brownfield path has been selected, when setting up the integration, packaging XCFramework or AAR artifacts, or adding React Native surfaces to native hosts.

This plugin packages the [`react-native-brownfield-migration`](skills/react-native-brownfield-migration/SKILL.md) skill from
[callstackincubator/agent-skills](https://github.com/callstackincubator/agent-skills/tree/main/skills/react-native-brownfield-migration) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/react-native-brownfield-migration/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install react-native-brownfield-migration@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dreact-native-brownfield-migration),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `react-native-brownfield-migration`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[callstackincubator/agent-skills](https://github.com/callstackincubator/agent-skills).
