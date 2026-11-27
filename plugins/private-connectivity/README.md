# private-connectivity

Set up private network connectivity to Grafana Cloud — AWS PrivateLink, Azure Private Link, GCP Private Service Connect, and Private Data Source Connect (PDC). Provisions VPC endpoints, private endpoints, or PSC forwarding rules per signal type (metrics / logs / traces / profiles); wires Alloy to push to the private DNS endpoint instead of the public one; verifies private DNS resolution + endpoint approval state. Use when sending telemetry to Grafana Cloud without traversing the public internet, eliminating cloud egress costs, meeting PCI-DSS / HIPAA / data-residency compliance, configuring PDC for private data-source queries, or connecting AWS / Azure / GCP workloads to Grafana — even when the user says "stop paying egress", "keep our telemetry off the public internet", or "PCI compliance for Grafana" without naming PrivateLink.

This plugin packages the [`private-connectivity`](skills/private-connectivity/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-cloud/private-connectivity) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/private-connectivity/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install private-connectivity@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dprivate-connectivity),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `private-connectivity`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
