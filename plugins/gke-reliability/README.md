# gke-reliability

Improves GKE workload reliability, using PDBs, health probes, and topology spread constraints. Use when configuring GKE workload reliability, setting up PDBs, or configuring GKE health probes (liveness, readiness, startup). Don't use for generating K8s YAML manifests (use gke-manifest-generation) or disaster recovery and cluster backups (use gke-backup-dr).

This plugin packages the [`gke-reliability`](skills/gke-reliability/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-reliability) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-reliability/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-reliability@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-reliability),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-reliability`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
