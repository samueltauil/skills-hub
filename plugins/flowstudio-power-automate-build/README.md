# flowstudio-power-automate-build

Build, scaffold, and deploy Power Automate cloud flows using the FlowStudio MCP server. Your agent constructs flow definitions, wires connections, deploys, and tests — all via MCP without opening the portal. Load this skill when asked to: create a flow, build a new flow, deploy a flow definition, scaffold a Power Automate workflow, construct a flow JSON, update an existing flow's actions, patch a flow definition, add actions to a flow, wire up connections, or generate a workflow definition from scratch. Requires a FlowStudio MCP subscription — see https://mcp.flowstudio.app

This plugin packages the [`flowstudio-power-automate-build`](skills/flowstudio-power-automate-build/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/flowstudio-power-automate-build) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/flowstudio-power-automate-build/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install flowstudio-power-automate-build@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dflowstudio-power-automate-build),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `flowstudio-power-automate-build`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
