# google-cloud-storage-fuse

Mounts Cloud Storage buckets on Google Cloud as a POSIX file system with Cloud Storage FUSE (gcsfuse). Use when interacting with gcsfuse or Cloud Storage FUSE mounts: decide whether FUSE, native gs:// reads, or Filestore/Managed Lustre fits a workload, deploy tuned mounts on GKE, Compute Engine, or Cloud Run, enable and size file, stat, and list caches, tune mount flags (--implicit-dirs) or config files, apply workload profiles, keep ML checkpointing safe (rename atomicity, hierarchical namespace/HNS, close-time finalization, concurrent writers), or diagnose slow training, low throughput, or bill spikes with gcsfuse metrics. Covers mount semantics, gcsfuse CLI and configs, GKE gcsfuse CSI driver (Workload Identity principal:// bindings, profile StorageClasses, sidecar sizing), and Cloud Run volume mounts. Don't use for bucket administration without a mount (google-cloud-storage-basics) or POSIX shared file systems (Filestore, Managed Lustre; use gke-storage).

This plugin packages the [`google-cloud-storage-fuse`](skills/google-cloud-storage-fuse/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/google-cloud-storage-fuse) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/google-cloud-storage-fuse/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install google-cloud-storage-fuse@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgoogle-cloud-storage-fuse),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `google-cloud-storage-fuse`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
