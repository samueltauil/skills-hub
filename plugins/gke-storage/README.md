# gke-storage

Manages GKE storage, including PVCs, PersistentVolumes, and Filestore. Use when configuring GKE storage or creating PVCs. For GCS FUSE mounts, use google-cloud-storage-fuse. For diagnosing storage failures (volume attach/mount errors, disk performance/node storage pressure, or Cloud Storage FUSE OOM), use gke-storage-troubleshooting. Don't use for database administration or replication strategies outside volume provisioning context.

This plugin packages the [`gke-storage`](skills/gke-storage/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-storage) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-storage/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-storage@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-storage),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-storage`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
