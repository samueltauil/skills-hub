# gke-cluster-autoscaler

Trigger on mention of GKE cluster autoscaler, node autoscaling, node pool auto-creation / node auto-provisioning. Provides guidance on enabling and optimizing cluster autoscaler, best practices, and troubleshooting issues such as nodes not scaling up or down, zonal stockouts, or capacity buffers. Do not use for ComputeClass-specific YAML generation or priority configuration (defer to gke-compute-classes skill).

This plugin packages the [`gke-cluster-autoscaler`](skills/gke-cluster-autoscaler/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-cluster-autoscaler) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-cluster-autoscaler/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-cluster-autoscaler@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-cluster-autoscaler),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-cluster-autoscaler`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
