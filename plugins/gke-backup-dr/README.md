# gke-backup-dr

Configures Backup for GKE: the BackupRestore cluster addon, BackupPlan and RestorePlan resources, restore workflows, and CMEK-encrypted backups. Use for backup policies, disaster recovery, or GKE cluster restores. Don't use for database backups.

This plugin packages the [`gke-backup-dr`](skills/gke-backup-dr/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-backup-dr) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-backup-dr/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-backup-dr@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-backup-dr),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-backup-dr`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
