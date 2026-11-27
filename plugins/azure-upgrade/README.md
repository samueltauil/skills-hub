# azure-upgrade

Assess and upgrade Azure workloads between plans, tiers, or SKUs, or modernize Azure SDK dependencies in source code. WHEN: upgrade Consumption to Flex Consumption, upgrade Azure Functions plan, change hosting plan, function app SKU, migrate App Service to Container Apps, modernize legacy Azure Java SDKs (com.microsoft.azure to com.azure), migrate Azure Cache for Redis (ACR/ACRE) to Azure Managed Redis (AMR).

This plugin packages the [`azure-upgrade`](skills/azure-upgrade/SKILL.md) skill from
[microsoft/azure-skills](https://github.com/microsoft/azure-skills/tree/main/.github/plugins/azure-skills/skills/azure-upgrade) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/azure-upgrade/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install azure-upgrade@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dazure-upgrade),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `azure-upgrade`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[microsoft/azure-skills](https://github.com/microsoft/azure-skills).
