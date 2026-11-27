# gke-cost-optimization

Optimizes GKE costs, rightsizes workloads, and configures Spot VMs, CUDs, cost allocation, and resource quotas. Use when optimizing GKE cluster or workload costs, configuring GKE cost allocation or quotas, rightsizing CPU/memory requests, or selecting Spot VMs and machine types. Don't use for general compute class provisioning or GPU Selection (use gke-compute-classes instead).

This plugin packages the [`gke-cost-optimization`](skills/gke-cost-optimization/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-cost-optimization) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-cost-optimization/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-cost-optimization@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-cost-optimization),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-cost-optimization`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
