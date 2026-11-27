# chatgpt-apps

Build, scaffold, refactor, and troubleshoot ChatGPT Apps SDK applications that combine an MCP server and widget UI. Use when Codex needs to design tools, register UI resources, wire the MCP Apps bridge or ChatGPT compatibility APIs, apply Apps SDK metadata or CSP or domain settings, or produce a docs-aligned project scaffold. Prefer a docs-first workflow by invoking the openai-docs skill or OpenAI developer docs MCP tools before generating code.

This plugin packages the [`chatgpt-apps`](skills/chatgpt-apps/SKILL.md) skill from
[openai/skills](https://github.com/openai/skills/tree/main/skills/.curated/chatgpt-apps) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/chatgpt-apps/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install chatgpt-apps@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dchatgpt-apps),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `chatgpt-apps`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[openai/skills](https://github.com/openai/skills).
