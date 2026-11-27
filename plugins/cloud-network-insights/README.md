# cloud-network-insights

Guides and automates setup, onboarding, synthetic monitoring operations, and cleanup for Cloud Network Insights in Google Cloud and Broadcom AppNeta. Use when enabling Cloud Network Insights, deploying or troubleshooting Monitoring Points across cloud and on-premises environments, configuring Network or Web monitoring policies and AppNeta alarm rules, configuring alert policies, querying path alarms and performance metrics, verifying synthetic path reachability, removing specific or all Monitoring Points, monitoring policies, and their hosts, or turning Cloud Network Insights off (only after warning the user and getting an explicit yes). Don't use for generic network observability, VPC Flow Logs, Cloud NAT, or VPC firewall debugging.

This plugin packages the [`cloud-network-insights`](skills/cloud-network-insights/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/cloud-network-insights) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/cloud-network-insights/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install cloud-network-insights@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcloud-network-insights),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `cloud-network-insights`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
