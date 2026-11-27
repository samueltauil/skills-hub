# gke-unprotected-statefulset

Audits, detects, and proposes fixes for GKE StatefulSets that lack a matching PodDisruptionBudget (PDB) to prevent simultaneous Pod evictions during voluntary node drains (GKE insight subtype PDB_UNPROTECTED_STATEFULSET). Use when investigating the PDB_UNPROTECTED_STATEFULSET insight, checking whether GKE StatefulSets have a matching PDB, or proposing fixes for selector mismatches where an existing PDB does not match the StatefulSet's .spec.selector. Don't use for existing PDBs that allow zero disruptions or block node drains (PDB_UNPERMISSIVE), general probe and PDB setup unrelated to this insight (use gke-reliability), upgrade planning (use gke-upgrades), Pods stuck in Pending (use gke-workload-troubleshooting), node autoscaling or capacity stockouts (use gke-cluster-autoscaler), ComputeClass configuration (use gke-compute-classes), or general Kubernetes manifest generation (use gke-manifest-generation).

This plugin packages the [`gke-unprotected-statefulset`](skills/gke-unprotected-statefulset/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-unprotected-statefulset) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-unprotected-statefulset/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-unprotected-statefulset@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-unprotected-statefulset),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-unprotected-statefulset`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
