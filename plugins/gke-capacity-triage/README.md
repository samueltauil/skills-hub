# gke-capacity-triage

Triage a GKE workload stuck Pending because node provisioning fails with a Compute Engine capacity error (ZONE_RESOURCE_POOL_EXHAUSTED, "GCE out of resources", scale.up.error.out.of.resources) or a quota error (QUOTA_EXCEEDED). Separates resource unavailability from quota limits and configuration causes, explains why the ComputeClass fallback didn't help, and gives the documented ComputeClass, Pod-level, or cluster-level fix to apply. Use when a user pastes a scale-up failure alert or asks why Pods are stuck Pending, lack nodes, or hit a stockout. Don't use for Standard-cluster TPU slices whose specific reservation lacks consumable instances, such as one held by unhealthy node pools with auto-repair disabled (gke-ai-troubleshooting-tpu-reservation-stockout), autoscaler enablement, profiles, or scale-down (gke-cluster-autoscaler), ComputeClass authoring without an incident (gke-compute-classes), Pods already on a node (gke-workload-troubleshooting, gke-storage-troubleshooting), or non-GKE clusters.

This plugin packages the [`gke-capacity-triage`](skills/gke-capacity-triage/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-capacity-triage) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-capacity-triage/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-capacity-triage@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-capacity-triage),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-capacity-triage`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
