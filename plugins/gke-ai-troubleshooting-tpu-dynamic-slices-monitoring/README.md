# gke-ai-troubleshooting-tpu-dynamic-slices-monitoring

Monitors, troubleshoots, and manages GKE TPU Dynamic Slices custom resources. Use when checking TPU slice lifecycle states, troubleshooting slice provisioning failures, validating single-slice or multi-slice (JobSet) workload manifests, or safely patching stuck finalizers and disabling the slice controller. Don't use for generic GKE cluster node pool creation or standard non-TPU workload management (use gke-basics or gke-cluster-creation instead).

This plugin packages the [`gke-ai-troubleshooting-tpu-dynamic-slices-monitoring`](skills/gke-ai-troubleshooting-tpu-dynamic-slices-monitoring/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-ai-troubleshooting-tpu-dynamic-slices-monitoring) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-ai-troubleshooting-tpu-dynamic-slices-monitoring/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-ai-troubleshooting-tpu-dynamic-slices-monitoring@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-ai-troubleshooting-tpu-dynamic-slices-monitoring),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-ai-troubleshooting-tpu-dynamic-slices-monitoring`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
