# docker-sandboxes-kits

Use this skill when authoring, verifying, publishing, or composing a Docker Sandboxes kit, even if the user just says they want to "add a tool to a sandbox agent", "package a CLI or agent as a kit", "publish a kit to a registry", or "give a mixin its own credentials and network access". Covers the v3 kit descriptor (`# syntax=docker/sandbox-kit:3`, `kind: workload` or `mixin`, typed capabilities, provides/requires, content recipes), building with docker buildx, checking with kit-tck and `sbx kit inspect`, composing onto a workload, referencing and pinning a kit from an `sbxenv.yaml` `agent:`/`kits:` entry, and publishing and signing. Legacy v2 `spec.yaml` kits are not covered; `sbx kit validate` is not a substitute for kit-tck conformance and runtime checks.

This plugin packages the [`docker-sandboxes-kits`](skills/docker-sandboxes-kits/SKILL.md) skill from
[docker/skills](https://github.com/docker/skills/tree/main/skills/docker-sandboxes-kits) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/docker-sandboxes-kits/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install docker-sandboxes-kits@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddocker-sandboxes-kits),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `docker-sandboxes-kits`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[docker/skills](https://github.com/docker/skills).
