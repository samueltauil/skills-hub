# gke-storage-troubleshooting

Diagnoses GKE persistent-storage failures — volume attach/mount errors (Regional PD on optimized VMs, fsGroup mount timeouts), disk-performance and node storage-pressure issues, slow-disk Pod-creation failures, volume-expansion problems, Local SSD / Hyperdisk Storage Pool creation errors, and Cloud Storage FUSE OOM. Use when Pods are stuck in ContainerCreating, volumes fail to attach or mount, or nodes report storage pressure. Don't use for routine storage provisioning or StorageClass/PVC authoring (see the gke-storage skill).

This plugin packages the [`gke-storage-troubleshooting`](skills/gke-storage-troubleshooting/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-storage-troubleshooting) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-storage-troubleshooting/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-storage-troubleshooting@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-storage-troubleshooting),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-storage-troubleshooting`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
