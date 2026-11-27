# docker-agent-deploy

Use this skill when exposing a Docker Agent as a server (MCP, HTTP API, A2A, ACP, or OpenAI-compatible chat), distributing an agent via an OCI registry with `docker agent share`, or measuring agent quality with `docker agent eval`. Even if the user just says they want to "turn my agent into an MCP server", "let Claude Desktop use my agent", "publish my agent to Docker Hub", "push my agent like an image", or "test my agent in CI", this skill applies. Covers `serve mcp/api/a2a/acp/chat` listen addresses and auth flags, `share push/pull`, eval session JSON format, scoring metrics, and the `--baseline` regression gate.

This plugin packages the [`docker-agent-deploy`](skills/docker-agent-deploy/SKILL.md) skill from
[docker/skills](https://github.com/docker/skills/tree/main/skills/docker-agent-deploy) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/docker-agent-deploy/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install docker-agent-deploy@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddocker-agent-deploy),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `docker-agent-deploy`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[docker/skills](https://github.com/docker/skills).
