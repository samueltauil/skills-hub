# azure-resource-health-diagnose

Analyze Azure resource health, diagnose issues from logs and telemetry, and create a remediation plan for identified problems.

This plugin packages the [`azure-resource-health-diagnose`](skills/azure-resource-health-diagnose/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/azure-resource-health-diagnose) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/azure-resource-health-diagnose/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install azure-resource-health-diagnose@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dazure-resource-health-diagnose),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `azure-resource-health-diagnose`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
