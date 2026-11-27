# gke-ai-troubleshooting-tpu-partition-overlap

Diagnose and resolve GKE TPU slice creation failures (SliceCreationFailed) caused by partition overlap conflicts where requested TPU partitions or their nodes are already used by another slice or JobSet. Use when diagnosing GKE TPU slice creation failures with SliceCreationFailed partition or node conflicts. Don't use for general slice lifecycle states or slice provisioning failures without node overlap (use gke-ai-troubleshooting-tpu-dynamic-slices-monitoring), quota exhaustion, or unresponsive TPU nodes.

This plugin packages the [`gke-ai-troubleshooting-tpu-partition-overlap`](skills/gke-ai-troubleshooting-tpu-partition-overlap/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-ai-troubleshooting-tpu-partition-overlap) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-ai-troubleshooting-tpu-partition-overlap/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-ai-troubleshooting-tpu-partition-overlap@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-ai-troubleshooting-tpu-partition-overlap),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-ai-troubleshooting-tpu-partition-overlap`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
