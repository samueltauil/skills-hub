# mcp-security-audit

Audit MCP (Model Context Protocol) server configurations for security issues. Use this skill when: - Reviewing .mcp.json files for security risks - Checking MCP server args for hardcoded secrets or shell injection patterns - Validating that MCP package-runner dependencies use exact reviewed versions, not bare names, @latest, or ranges - Detecting mutable npm/npx, bunx, pnpm dlx, yarn dlx, npm exec, uvx, uv tool run, and pipx run references in MCP configurations - Auditing which MCP servers a project registers and whether they're on an approved list - Checking for environment variable usage vs. hardcoded credentials in MCP configs - Any request like "is my MCP config secure?", "audit my MCP servers", or "check .mcp.json" keywords: [mcp, security, audit, secrets, shell-injection, supply-chain, governance]

This plugin packages the [`mcp-security-audit`](skills/mcp-security-audit/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/mcp-security-audit) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/mcp-security-audit/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install mcp-security-audit@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmcp-security-audit),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `mcp-security-audit`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
