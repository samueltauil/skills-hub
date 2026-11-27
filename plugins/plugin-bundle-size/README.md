# plugin-bundle-size

Optimise Grafana app plugin bundle size using React.lazy, Suspense, and webpack code splitting. Use when the user asks to reduce plugin bundle size, optimise module.js, add code splitting, improve initial plugin load performance, split plugin chunks, lazy load plugin pages, or help implement lazy loading in a Grafana app plugin. Triggers on phrases like "optimise plugin bundle size", "module.js is too large", "plugin is slow to load", "code split the plugin", "reduce initial JS payload", or "help me with Suspense in my plugin".

This plugin packages the [`plugin-bundle-size`](skills/plugin-bundle-size/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-plugins/plugin-bundle-size) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/plugin-bundle-size/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install plugin-bundle-size@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dplugin-bundle-size),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `plugin-bundle-size`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
