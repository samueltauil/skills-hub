# google-cloud-filestore-log-troubleshooting

Diagnoses and resolves Filestore client mount failures on Google Cloud, permission errors (EACCES), and network timeouts (ETIMEDOUT). Use when an NFS mount hangs or fails from a Compute Engine VM, GKE pod, Cloud Run service, or Vertex AI workload, when `mount.nfs` reports "Connection timed out" or "access denied by server", when checking whether VPC ingress firewall rules or `nfsExportOptions` allow a client IP, or when a previously working Filestore share suddenly stops mounting after an administrative change. Don't use for Cloud Storage (GCS) buckets, Persistent Disk, or Cloud NetApp Volumes, and don't use for Filestore capacity scaling or backup and export-policy auditing.

This plugin packages the [`google-cloud-filestore-log-troubleshooting`](skills/google-cloud-filestore-log-troubleshooting/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/google-cloud-filestore-log-troubleshooting) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/google-cloud-filestore-log-troubleshooting/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install google-cloud-filestore-log-troubleshooting@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgoogle-cloud-filestore-log-troubleshooting),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `google-cloud-filestore-log-troubleshooting`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
