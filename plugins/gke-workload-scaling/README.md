# gke-workload-scaling

Manages scaling for GKE workloads using HPA and VPA. Use when configuring Horizontal Pod Autoscaler (HPA), configuring Vertical Pod Autoscaler (VPA), or applying best practices for GKE workload autoscaling. Do not use for cluster-level autoscaling (Cluster Autoscaler), static cluster sizing, or configuring node-level machine styles directly.

This plugin packages the [`gke-workload-scaling`](skills/gke-workload-scaling/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-workload-scaling) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-workload-scaling/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-workload-scaling@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-workload-scaling),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-workload-scaling`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
