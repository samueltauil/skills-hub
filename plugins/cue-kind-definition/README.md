# cue-kind-definition

Author CUE kind definitions for grafana-app-sdk apps - schemas, versioning, field constraints, named type definitions, custom routes, and codegen configuration. Scaffolds kinds via `grafana-app-sdk project kind add`, writes spec/status schemas with type constraints (regex, enum, range), defines `#`-prefixed named types for reusable structs, registers versions in the app manifest, and runs `grafana-app-sdk generate` with explicit error recovery. Use when working with CUE kinds, adding a new resource type, adding a version to an existing kind, writing schema field constraints, defining `#Definition` types, adding custom routes, editing files under `kinds/`, or when the user asks to "model a resource", "add a CUE schema", or "write a kind" — even without saying "CUE" explicitly.

This plugin packages the [`cue-kind-definition`](skills/cue-kind-definition/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-app-sdk/cue-kind-definition) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/cue-kind-definition/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install cue-kind-definition@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcue-kind-definition),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `cue-kind-definition`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
