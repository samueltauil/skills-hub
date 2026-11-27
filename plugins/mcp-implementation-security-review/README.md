# mcp-implementation-security-review

Review the implementation source code of MCP (Model Context Protocol) servers, clients, and tool handlers against a security baseline — authentication, sessions, rate limiting, input-schema validation, official-SDK usage, RCE vectors, and the OWASP MCP Top 10 — producing a report with file/line evidence. Use this skill when: - Reviewing an MCP server implementation for security before release - Checking a server against the baseline controls (MCP-01 to MCP-05) and the OWASP MCP Top 10 - Auditing tools for RCE vectors (command/code injection, unsafe deserialization, path traversal, SSTI, dependency hijacking, SSRF) - Verifying auth, session, rate-limiting, and input-validation controls on a network-exposed server - Reviewing MCP client code that handles untrusted server responses and session IDs - Requests like "review this MCP server for security" or "is my MCP server implementation secure?"

This plugin packages the [`mcp-implementation-security-review`](skills/mcp-implementation-security-review/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/mcp-implementation-security-review) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/mcp-implementation-security-review/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install mcp-implementation-security-review@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmcp-implementation-security-review),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `mcp-implementation-security-review`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
