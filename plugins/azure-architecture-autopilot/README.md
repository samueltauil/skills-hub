# azure-architecture-autopilot

Design Azure infrastructure using natural language, or analyze existing Azure resources to auto-generate architecture diagrams, refine them through conversation, and deploy with Bicep. When to use this skill: - "Create X on Azure", "Set up a RAG architecture" (new design) - "Analyze my current Azure infrastructure", "Draw a diagram for rg-xxx" (existing analysis) - "Foundry is slow", "I want to reduce costs", "Strengthen security" (natural language modification) - Azure resource deployment, Bicep template generation, IaC code generation - Microsoft Foundry, AI Search, OpenAI, Fabric, ADLS Gen2, Databricks, and all Azure services

This plugin packages the [`azure-architecture-autopilot`](skills/azure-architecture-autopilot/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/azure-architecture-autopilot) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/azure-architecture-autopilot/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install azure-architecture-autopilot@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dazure-architecture-autopilot),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `azure-architecture-autopilot`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
