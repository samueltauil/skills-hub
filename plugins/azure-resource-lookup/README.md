# azure-resource-lookup

List, find, and show Azure resources across subscriptions or resource groups. Handles prompts like "list the websites in my subscription", "list my web apps", "show my app services", "list virtual machines", "list my VMs", "show storage accounts", "find container apps", and "what resources do I have". USE FOR: list websites, list web apps, list app services, show websites in subscription, resource inventory, find resources by tag, tag analysis, orphaned resource discovery (not for cost analysis), unattached disks, count resources by type, cross-subscription lookup, and Azure Resource Graph queries. DO NOT USE FOR: deploying/changing resources (use azure-deploy), cost optimization (use cost-optimization from the optional azure-cost plugin), or non-Azure clouds.

This plugin packages the [`azure-resource-lookup`](skills/azure-resource-lookup/SKILL.md) skill from
[microsoft/azure-skills](https://github.com/microsoft/azure-skills/tree/main/.github/plugins/azure-skills/skills/azure-resource-lookup) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/azure-resource-lookup/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install azure-resource-lookup@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dazure-resource-lookup),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `azure-resource-lookup`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[microsoft/azure-skills](https://github.com/microsoft/azure-skills).
