# docker-agent-config

Use this skill when creating or editing an agent.yaml (or .yml/.hcl) configuration file for Docker Agent (cagent), including defining agents, models/providers, built-in or MCP toolsets, multi-agent teams with sub_agents. Even if the user just says they want to "build an AI agent with Docker", "make a coding agent config", "add a tool to my agent", or "set up a team of agents", this skill applies. Covers agent properties (model, instruction, toolsets, sub_agents, fallback), the models/providers sections, built-in toolsets (filesystem, shell, think, todo, memory, fetch), MCP toolset references, and named commands.

This plugin packages the [`docker-agent-config`](skills/docker-agent-config/SKILL.md) skill from
[docker/skills](https://github.com/docker/skills/tree/main/skills/docker-agent-config) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/docker-agent-config/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install docker-agent-config@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddocker-agent-config),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `docker-agent-config`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[docker/skills](https://github.com/docker/skills).
