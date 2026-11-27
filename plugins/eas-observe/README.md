# eas-observe

Use for anything related to EAS Observe - adding `expo-observe` to an Expo project (ObserveRoot/AppMetricsRoot, markInteractive, useObserve, ObserveInteractiveMarker, the Expo Router / React Navigation integrations for per-route metrics, the expo-image and Reanimated integrations, `Observe.logEvent` events, error reporting via ObserveErrorBoundary and `Observe.reportError`, native crashes, source map and iOS dSYM upload for symbolication, network traces, and config such as sampleRate, errorSampleRate and networkTraces), querying via the EAS CLI (`eas observe:metrics-summary`, `observe:metrics`, `observe:routes`, `observe:events`, `observe:session`, `observe:versions`, `observe:errors`, `observe:traces`, `observe:trace`, `observe:event`) or the Expo MCP `observe_*` tools, interpreting the results (cold/warm launch, TTR, TTI, navigation TTR, update download, and the TTI frameRate/device/network params for slow startups), or shipping an Observe integration inside a third-party package.

This plugin packages the [`eas-observe`](skills/eas-observe/SKILL.md) skill from
[expo/skills](https://github.com/expo/skills/tree/main/plugins/expo/skills/eas-observe) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/eas-observe/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install eas-observe@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Deas-observe),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `eas-observe`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[expo/skills](https://github.com/expo/skills).
