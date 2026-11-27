# gke-compute-classes

Configures, optimizes, and troubleshoots GKE ComputeClasses. Use when configuring Spot VMs with on-demand fallback, targeting specific accelerators (GPUs/TPUs) or machine families, restricting ComputeClass access, or debugging pending pods related to node pool auto-creation. Do not use for cluster-level Node Auto Provisioning configuration or general GKE cluster creation.

This plugin packages the [`gke-compute-classes`](skills/gke-compute-classes/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-compute-classes) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-compute-classes/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-compute-classes@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-compute-classes),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-compute-classes`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
