# gke-ai-troubleshooting-tpu-metrics-monitoring

Monitors and troubleshoots GKE TPU workloads, nodes, and node pools using GKE system metrics and PromQL. Use when monitoring TensorCore duty cycle, TPU memory, node readiness, multi-host TPU node pool availability, host maintenance or preemption interruptions, and calculating MTTR or MTBI metrics for GKE TPUs. Don't use for general non-TPU GKE workload monitoring or non-metric TPU debugging.

This plugin packages the [`gke-ai-troubleshooting-tpu-metrics-monitoring`](skills/gke-ai-troubleshooting-tpu-metrics-monitoring/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-ai-troubleshooting-tpu-metrics-monitoring) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-ai-troubleshooting-tpu-metrics-monitoring/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-ai-troubleshooting-tpu-metrics-monitoring@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-ai-troubleshooting-tpu-metrics-monitoring),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-ai-troubleshooting-tpu-metrics-monitoring`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
