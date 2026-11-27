# gke-workload-scaling-troubleshooting

Diagnoses GKE HorizontalPodAutoscaler (HPA) failures — metrics showing as <unknown>, FailedGetResourceMetric / FailedGetScale / FailedComputeMetricsReplicas events, missing Pod resource requests, custom/external metrics-pipeline breakage (FailedGetExternalMetric / FailedGetCustomMetric, unavailable metrics adapter, control-plane firewall blocking the adapter), HPA that won't scale up or down (tolerance / stabilization window / unavailable rate metrics), scale-to/from-zero problems, and slow HPA reaction on large clusters. Use when an HPA isn't scaling a workload as expected or reports metric errors. Don't use for configuring or authoring new HPA/VPA objects or scaling best practices (see the gke-workload-scaling skill), or for Cluster Autoscaler / node-pool sizing.

This plugin packages the [`gke-workload-scaling-troubleshooting`](skills/gke-workload-scaling-troubleshooting/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-workload-scaling-troubleshooting) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-workload-scaling-troubleshooting/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-workload-scaling-troubleshooting@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-workload-scaling-troubleshooting),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-workload-scaling-troubleshooting`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
