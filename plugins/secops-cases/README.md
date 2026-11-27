# secops-cases

Manage Google Security Operations (SecOps) SOAR cases throughout their lifecycle. Use when listing, creating, inspecting, updating, or closing SOAR cases; adding investigative comments and notes; updating case priority or description; or linking and grouping security alerts within cases. Supports both remote Google SecOps MCP tools and local fallback tools. Don't use for SIEM UDM searches or detection rule authoring.

This plugin packages the [`secops-cases`](skills/secops-cases/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/secops-cases) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/secops-cases/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install secops-cases@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsecops-cases),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `secops-cases`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
