# suggest-awesome-github-copilot-agents

Suggest relevant GitHub Copilot Custom Agents files from the awesome-copilot repository based on current repository context and chat history, avoiding duplicates with existing custom agents in this repository, and identifying outdated agents that need updates.

This plugin packages the [`suggest-awesome-github-copilot-agents`](skills/suggest-awesome-github-copilot-agents/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/suggest-awesome-github-copilot-agents) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/suggest-awesome-github-copilot-agents/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install suggest-awesome-github-copilot-agents@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsuggest-awesome-github-copilot-agents),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `suggest-awesome-github-copilot-agents`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
