# foundry-hosted-agent-copilotkit

Build and evolve agentic web apps that pair a CopilotKit React frontend with a Microsoft Agent Framework agent running as a Microsoft Foundry hosted agent, connected over the AG-UI protocol. Covers choosing the wiring, using Foundry-native primitives instead of hand-rolled plumbing, agent tools, human-in-the-loop approvals, generative UI and shared state, local run and azd deploy, debugging the event stream, and safe upgrades.

This plugin packages the [`foundry-hosted-agent-copilotkit`](skills/foundry-hosted-agent-copilotkit/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/foundry-hosted-agent-copilotkit) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/foundry-hosted-agent-copilotkit/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install foundry-hosted-agent-copilotkit@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dfoundry-hosted-agent-copilotkit),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `foundry-hosted-agent-copilotkit`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
