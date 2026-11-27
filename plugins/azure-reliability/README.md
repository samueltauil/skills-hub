# azure-reliability

Assess and improve the reliability posture of PaaS Applications (Azure Functions and Azure App Service). Scans deployed resources for zone redundancy, ZRS storage, health probes, and multi-region failover. Presents a feature-pivoted checklist, then drives staged remediation (CLI or IaC patches) end-to-end with user confirmation. WHEN: "assess reliability", "check reliability", "zone redundant", "multi-region failover", "high availability", "disaster recovery", "single points of failure", "reliability posture", "resiliency".

This plugin packages the [`azure-reliability`](skills/azure-reliability/SKILL.md) skill from
[microsoft/azure-skills](https://github.com/microsoft/azure-skills/tree/main/.github/plugins/azure-skills/skills/azure-reliability) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/azure-reliability/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install azure-reliability@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dazure-reliability),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `azure-reliability`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[microsoft/azure-skills](https://github.com/microsoft/azure-skills).
