# gke-node-notready

Diagnoses GKE nodes reporting NotReady or Unknown status by inspecting node conditions, events, kubelet/containerd logs, and node metrics, then proposing safe remediations. Use when nodes show NotReady, when the kubelet stops posting node status, or when workloads are evicted or stuck Pending due to node health. Don't use for pod-level application failures (use gke-workload-troubleshooting), autoscaler scale-up/scale-down decisions (use gke-cluster-autoscaler), or non-GKE compute.

This plugin packages the [`gke-node-notready`](skills/gke-node-notready/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-node-notready) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-node-notready/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-node-notready@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-node-notready),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-node-notready`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
