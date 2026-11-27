# gke-ai-troubleshooting-handle-disruption-gpu-tpu

Diagnoses, predicts, and mitigates node disruptions during Compute Engine host maintenance and hardware or software maintenance events for GPU and TPU workloads on GKE. Use when diagnosing node disruptions, predicting host maintenance events on GPU/TPU nodepools, inspecting node interruption PromQL metrics, auditing node taints, or configuring workload protection strategies (graceful termination, opportunistic maintenance, PodDisruptionBudgets). Don't use for general GKE cluster creation, network policy configuration, or non-disruption workload deployment.

This plugin packages the [`gke-ai-troubleshooting-handle-disruption-gpu-tpu`](skills/gke-ai-troubleshooting-handle-disruption-gpu-tpu/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-ai-troubleshooting-handle-disruption-gpu-tpu) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-ai-troubleshooting-handle-disruption-gpu-tpu/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-ai-troubleshooting-handle-disruption-gpu-tpu@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-ai-troubleshooting-handle-disruption-gpu-tpu),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-ai-troubleshooting-handle-disruption-gpu-tpu`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
