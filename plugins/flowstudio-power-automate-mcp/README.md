# flowstudio-power-automate-mcp

Foundation skill for Power Automate via FlowStudio MCP — auth setup, the reusable MCP helper (Python + Node.js), tool discovery via `list_skills` / `tool_search`, and oversized-response handling. Load this skill first when connecting an agent to Power Automate. For specialized workflows, load `flowstudio-power-automate-build`, `flowstudio-power-automate-debug`, `flowstudio-power-automate-monitoring` (Pro+), or `flowstudio-power-automate-governance` (Pro+) — each contains the workflow narrative, this skill provides the plumbing they all rely on. Requires a FlowStudio MCP subscription or compatible server — see https://mcp.flowstudio.app

This plugin packages the [`flowstudio-power-automate-mcp`](skills/flowstudio-power-automate-mcp/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/flowstudio-power-automate-mcp) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/flowstudio-power-automate-mcp/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install flowstudio-power-automate-mcp@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dflowstudio-power-automate-mcp),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `flowstudio-power-automate-mcp`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
