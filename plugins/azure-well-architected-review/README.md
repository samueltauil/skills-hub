# azure-well-architected-review

Perform an Azure Well-Architected Framework review of the current workload IaC and architecture, generating findings and GitHub issues for improvements.

This plugin packages the [`azure-well-architected-review`](skills/azure-well-architected-review/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/azure-well-architected-review) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/azure-well-architected-review/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install azure-well-architected-review@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dazure-well-architected-review),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `azure-well-architected-review`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
