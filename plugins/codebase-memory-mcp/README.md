# codebase-memory-mcp

Use when exploring unfamiliar code, mapping architecture, finding symbols or relationships, tracing callers, callees, data flow or dependencies, assessing impact, auditing dead or complex code, or handling explicit Codebase Memory requests. Otherwise skip tasks confined to a supplied known file, tiny one-file check, exact literal, configuration value, error string, or non-code text.

This plugin packages the [`codebase-memory-mcp`](skills/codebase-memory-mcp/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/codebase-memory-mcp) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/codebase-memory-mcp/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install codebase-memory-mcp@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcodebase-memory-mcp),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `codebase-memory-mcp`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
