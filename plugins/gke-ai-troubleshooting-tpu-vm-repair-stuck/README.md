# gke-ai-troubleshooting-tpu-vm-repair-stuck

Diagnose GKE TPU VM instances stuck in Compute Engine repair (REPAIRING state) after host errors, maintenance events, or faulty host reports in single-host, multi-host, dynamic slicing, and TPU All Capacity mode node pools. Use when TPU instances in a slice node pool remain in REPAIRING, host error events appear in audit logs, or TPU slices are unschedulable due to a VM in repair. Don't use for nodes reporting Ready: Unknown when no VM is in REPAIRING (use gke-ai-troubleshooting-node-unresponsive-timeout), other NotReady nodes when no VM is in REPAIRING (use gke-node-notready), Pending Pods when all nodes are Ready (use gke-workload-troubleshooting), JobSet preemption events (use gke-ai-troubleshooting-jobset-interruption), or Slice custom resource lifecycle failures (use gke-ai-troubleshooting-tpu-dynamic-slices-monitoring).

This plugin packages the [`gke-ai-troubleshooting-tpu-vm-repair-stuck`](skills/gke-ai-troubleshooting-tpu-vm-repair-stuck/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-ai-troubleshooting-tpu-vm-repair-stuck) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-ai-troubleshooting-tpu-vm-repair-stuck/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-ai-troubleshooting-tpu-vm-repair-stuck@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-ai-troubleshooting-tpu-vm-repair-stuck),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-ai-troubleshooting-tpu-vm-repair-stuck`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
