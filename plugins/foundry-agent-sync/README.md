# foundry-agent-sync

Create and synchronize prompt-based AI agents directly within Azure AI Foundry via REST API, from a local JSON manifest. Unlike scaffolding skills that only generate local code, this skill registers agents in the Foundry service itself — making them immediately available for invocation. Use when the user asks to create agents in Foundry, sync, deploy, register, or push agents to Foundry, update agent instructions, or scaffold the manifest and sync script for a new repository. Triggers: 'create agent in foundry', 'sync foundry agents', 'deploy agents to foundry', 'register agents in foundry', 'push agents', 'create foundry agent manifest', 'scaffold agent sync'.

This plugin packages the [`foundry-agent-sync`](skills/foundry-agent-sync/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/foundry-agent-sync) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/foundry-agent-sync/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install foundry-agent-sync@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dfoundry-agent-sync),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `foundry-agent-sync`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
