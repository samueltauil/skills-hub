# upgrading-react-native

Upgrades React Native apps to newer versions by applying rn-diff-purge template diffs, updating package.json dependencies, migrating native iOS and Android configuration, resolving CocoaPods and Gradle changes, and handling breaking API updates. Use when upgrading React Native, bumping RN version, updating from RN 0.x to 0.y, or migrating Expo SDK alongside a React Native upgrade.

This plugin packages the [`upgrading-react-native`](skills/upgrading-react-native/SKILL.md) skill from
[callstackincubator/agent-skills](https://github.com/callstackincubator/agent-skills/tree/main/skills/upgrading-react-native) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/upgrading-react-native/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install upgrading-react-native@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dupgrading-react-native),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `upgrading-react-native`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[callstackincubator/agent-skills](https://github.com/callstackincubator/agent-skills).
