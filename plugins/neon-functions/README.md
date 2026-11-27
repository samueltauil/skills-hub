# neon-functions

Long-running, serverless Node.js HTTP functions deployed onto your Neon branch, with DATABASE_URL injected automatically and compute that runs next to your data. Use when a user wants to host an API, an AI agent with long streaming responses, a WebSocket or server-sent-events (SSE) server, a webhook handler, a Discord bot, an MCP server, or any request/response workload that risks timing out on short, lambda-style serverless functions — and wants it to branch with their database. Also use for Function Triggers: a cron or an object-storage event that POSTs to a function. Triggers include "serverless function", "deploy an API", "long-running function", "streaming agent", "SSE server", "WebSocket server", "webhook handler", "MCP server", "cron", "scheduled function", "object storage trigger", "on upload", "function that won't time out", "function logs", "Neon Functions", "Neon Compute", "DDoS protection", "rate limiting", and "production hardening". For live UIs over database rows, use neon-realtime.

This plugin packages the [`neon-functions`](skills/neon-functions/SKILL.md) skill from
[neondatabase/agent-skills](https://github.com/neondatabase/agent-skills/tree/main/skills/neon-functions) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/neon-functions/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install neon-functions@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dneon-functions),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `neon-functions`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[neondatabase/agent-skills](https://github.com/neondatabase/agent-skills).
