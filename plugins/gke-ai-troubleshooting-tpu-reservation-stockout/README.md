# gke-ai-troubleshooting-tpu-reservation-stockout

Diagnose and resolve cluster-wide GKE TPU node pool creation or scale-up failures caused by Compute Engine reservation stockouts (GCE_STOCKOUT, ZONE_RESOURCE_POOL_EXHAUSTED) when existing unhealthy or NotReady TPU node pools in the cluster have node auto-repair disabled and hold reserved TPU capacity. Use when TPU node pool creation or scale-up fails with GCE_STOCKOUT, ZONE_RESOURCE_POOL_EXHAUSTED, or ZONE_RESOURCE_POOL_EXHAUSTED_WITH_DETAILS despite having a specific Compute Engine TPU reservation. Don't use for general pod scheduling without a TPU reservation or workload-level container crashes.

This plugin packages the [`gke-ai-troubleshooting-tpu-reservation-stockout`](skills/gke-ai-troubleshooting-tpu-reservation-stockout/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-ai-troubleshooting-tpu-reservation-stockout) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-ai-troubleshooting-tpu-reservation-stockout/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-ai-troubleshooting-tpu-reservation-stockout@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-ai-troubleshooting-tpu-reservation-stockout),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-ai-troubleshooting-tpu-reservation-stockout`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
