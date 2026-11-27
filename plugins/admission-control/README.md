# admission-control

Use when the user asks to "write a validator", "add validation", "implement admission control", "write a mutating webhook", "add a mutation handler", "validate incoming resources", "implement admission logic", "add admission webhooks", "write ingress validation", or asks how to validate or mutate resources before they are persisted in a grafana-app-sdk app. Provides guidance on implementing validation and mutation admission handlers for grafana-app-sdk apps.

This plugin packages the [`admission-control`](skills/admission-control/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-app-sdk/admission-control) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/admission-control/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install admission-control@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dadmission-control),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `admission-control`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
