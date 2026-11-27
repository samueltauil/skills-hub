# gke-kueue-troubleshooting

Diagnose a GKE batch or AI workload (Job, JobSet, LeaderWorkerSet, RayJob, Kubeflow training jobs, or plain Pods) that is pending, suspended, stuck, evicted or misconfigured when Kueue manages it - from a live GKE cluster, a support bundle or exported controller/audit logs. Load it as soon as the investigation shows a Kueue footprint, even if the user never said "Kueue" - anything under kueue.x-k8s.io (labels, Pod scheduling gates, Workload/LocalQueue/ClusterQueue objects and their conditions), kueue-controller-manager events or logs, or a Job with spec.suspend=true together with a Workload object in its namespace. Scripts compact cluster state and logs into verifiable facts and validate the report, while the agent classifies the cause as Kueue configuration, Kueue defect, or outside Kueue. Don't use for workloads with no Kueue footprint (use gke-node-notready, gke-workload-scaling-troubleshooting, gke-ai-troubleshooting-tpu-reservation-stockout, or gke-ai-troubleshooting-jobset-interruption).

This plugin packages the [`gke-kueue-troubleshooting`](skills/gke-kueue-troubleshooting/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-kueue-troubleshooting) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-kueue-troubleshooting/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-kueue-troubleshooting@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-kueue-troubleshooting),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-kueue-troubleshooting`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
