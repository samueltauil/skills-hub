# grafana-scenes

Build Grafana plugin pages using the @grafana/scenes framework. Use when creating new scene pages, adding panels/visualizations, setting up drilldown navigation, defining variables, configuring query runners, building table/timeseries/stat panels, or extending SceneObjectBase for custom scene objects. Triggers on any work involving SceneApp, SceneAppPage, EmbeddedScene, SceneQueryRunner, SceneDataTransformer, PanelBuilders, SceneFlexLayout, QueryVariable, or drilldown/tab configuration in Grafana plugins.

This plugin packages the [`grafana-scenes`](skills/grafana-scenes/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-plugins/grafana-scenes) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/grafana-scenes/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install grafana-scenes@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgrafana-scenes),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `grafana-scenes`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
