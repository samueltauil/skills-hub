# azure-quotas

Check/manage Azure quotas and usage across providers. For deployment planning, capacity validation, region selection. WHEN: "check quotas", "service limits", "current usage", "request quota increase", "quota exceeded", "validate capacity", "regional availability", "provisioning limits", "vCPU limit", "how many vCPUs available in my subscription".

This plugin packages the [`azure-quotas`](skills/azure-quotas/SKILL.md) skill from
[microsoft/azure-skills](https://github.com/microsoft/azure-skills/tree/main/.github/plugins/azure-skills/skills/azure-quotas) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/azure-quotas/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install azure-quotas@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dazure-quotas),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `azure-quotas`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[microsoft/azure-skills](https://github.com/microsoft/azure-skills).
