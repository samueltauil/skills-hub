# gke-statefulset-without-probes

Audits, detects, and proposes fixes for GKE StatefulSets that are protected by a PodDisruptionBudget (PDB) but lack container readiness probes (GKE insight subtype PDB_STATEFULSET_WITHOUT_PROBES), causing replacement Pods to be counted as healthy before they are ready during voluntary disruptions. Use when asked to check, audit, or propose fixes for the PDB_STATEFULSET_WITHOUT_PROBES condition, missing readinessProbe configurations on PDB-protected GKE StatefulSets, or premature eviction of StatefulSet replicas during node pool upgrades or drains despite having a PDB. Don't use for StatefulSets missing a PDB (PDB_UNPROTECTED_STATEFULSET), PDBs that allow zero disruptions (PDB_UNPERMISSIVE), general probe and PDB setup unrelated to this condition (use gke-reliability), Pods stuck in Pending (use gke-workload-troubleshooting), ComputeClass configuration (use gke-compute-classes), manifest generation (use gke-manifest-generation), or cluster upgrade planning (use gke-upgrades).

This plugin packages the [`gke-statefulset-without-probes`](skills/gke-statefulset-without-probes/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-statefulset-without-probes) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-statefulset-without-probes/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-statefulset-without-probes@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-statefulset-without-probes),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-statefulset-without-probes`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
