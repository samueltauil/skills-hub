# agent-governance

Patterns and techniques for adding governance, safety, and trust controls to AI agent systems. Use this skill when: - Building AI agents that call external tools (APIs, databases, file systems) - Implementing policy-based access controls for agent tool usage - Adding semantic intent classification to detect dangerous prompts - Creating trust scoring systems for multi-agent workflows - Building audit trails for agent actions and decisions - Enforcing rate limits, content filters, or tool restrictions on agents - Working with any agent framework (PydanticAI, CrewAI, OpenAI Agents, LangChain, AutoGen)

This plugin packages the [`agent-governance`](skills/agent-governance/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/agent-governance) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/agent-governance/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install agent-governance@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dagent-governance),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `agent-governance`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
