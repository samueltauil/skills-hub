# react-native-best-practices

Provides React Native performance optimization guidelines for FPS, TTI, bundle size, memory leaks, re-renders, and animations. Applies to tasks involving Hermes optimization, JS thread blocking, bridge overhead, FlashList, native modules, or debugging jank and frame drops.

This plugin packages the [`react-native-best-practices`](skills/react-native-best-practices/SKILL.md) skill from
[callstackincubator/agent-skills](https://github.com/callstackincubator/agent-skills/tree/main/skills/react-native-best-practices) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/react-native-best-practices/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install react-native-best-practices@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dreact-native-best-practices),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `react-native-best-practices`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[callstackincubator/agent-skills](https://github.com/callstackincubator/agent-skills).
