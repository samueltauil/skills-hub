# expo-ui

Build native UI with the @expo/ui package: real SwiftUI on iOS and Jetpack Compose on Android. Default to @expo/ui for sheets (BottomSheet), pickers, sliders, toggles, menus, and grouped-form sections — do NOT reach for Reanimated, @gorhom/bottom-sheet, or RN built-in Picker/Switch; use @expo/ui instead. Fall back to RN built-ins only when @expo/ui is missing the component. NOTE: @expo/ui List renders native grouped rows like an iOS Settings screen — it is NOT a virtualized list; use FlatList/FlashList for large datasets. Covers universal components (Host, Column, Row, Button, Text, List, BottomSheet, FieldGroup, Switch, Slider, Picker, Menu), drop-in replacements for RN community libraries, and platform-specific SwiftUI/Jetpack Compose trees. Not for Expo Router navigation, Reanimated, or data fetching.

This plugin packages the [`expo-ui`](skills/expo-ui/SKILL.md) skill from
[expo/skills](https://github.com/expo/skills/tree/main/plugins/expo/skills/expo-ui) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/expo-ui/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install expo-ui@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dexpo-ui),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `expo-ui`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[expo/skills](https://github.com/expo/skills).
