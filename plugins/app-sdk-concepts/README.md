# app-sdk-concepts

Use when starting any grafana-app-sdk work — scaffolding a Grafana app, initializing a Grafana App Platform app, picking a deployment mode (standalone operator / grafana/apps / frontend-only), wiring app-specific config, or onboarding to the SDK. Covers `grafana-app-sdk` CLI install, `project init` per deployment mode, project layout, the schema-centric workflow (CUE kinds → generated code → reconciler/admission logic), and `SpecificConfig` for env-driven app configuration. Use even if the user just says "make a new app", "Grafana app platform", "kinds and watchers", "operator scaffold", or asks about `apps/` inside the Grafana repo, without naming the SDK explicitly.

This plugin packages the [`app-sdk-concepts`](skills/app-sdk-concepts/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-app-sdk/app-sdk-concepts) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/app-sdk-concepts/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install app-sdk-concepts@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dapp-sdk-concepts),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `app-sdk-concepts`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
