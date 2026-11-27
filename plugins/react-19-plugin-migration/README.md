# react-19-plugin-migration

Migrate a Grafana plugin to React 19 compatibility. Use when the user asks to update a plugin for React 19, prepare for React 19, fix React 19 compatibility, upgrade to React 19, migrate to React 19, bump grafanaDependency to 12.3.0, externalize jsx-runtime, or run react-detect. Triggers on phrases like "update plugin for React 19", "React 19 migration", "prepare for React 19", "plugin React 19 compat", "grafanaDependency 12.3.0", "JSX runtime externals", "react-detect", "SECRET_INTERNALS", "ReactCurrentOwner", or "ReactCurrentDispatcher".

This plugin packages the [`react-19-plugin-migration`](skills/react-19-plugin-migration/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-plugins/react-19-plugin-migration) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/react-19-plugin-migration/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install react-19-plugin-migration@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dreact-19-plugin-migration),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `react-19-plugin-migration`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
