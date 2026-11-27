# flowstudio-power-automate-debug

Debug failing Power Automate cloud flows using the FlowStudio MCP server. The Graph API only shows top-level status codes. This skill gives your agent action-level inputs and outputs to find the actual root cause. Load this skill when asked to: debug a flow, investigate a failed run, why is this flow failing, inspect action outputs, find the root cause of a flow error, fix a broken Power Automate flow, diagnose a timeout, trace a DynamicOperationRequestFailure, check connector auth errors, read error details from a run, or troubleshoot expression failures. Requires a FlowStudio MCP subscription — see https://mcp.flowstudio.app

This plugin packages the [`flowstudio-power-automate-debug`](skills/flowstudio-power-automate-debug/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/flowstudio-power-automate-debug) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/flowstudio-power-automate-debug/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install flowstudio-power-automate-debug@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dflowstudio-power-automate-debug),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `flowstudio-power-automate-debug`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
