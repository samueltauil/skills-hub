# google-cloud-filestore-auditing

Audits Filestore instances on Google Cloud across projects for disaster recovery readiness (missing or stale backups), security access governance (overly permissive NFS export rules, 0.0.0.0/0 exposure, missing ROOT_SQUASH), and reliability compliance (Physical Zone Isolation PZI and Physical Zone Separation PZS). Use when assessing storage health posture, auditing NFS export permissions, identifying unprotected file shares, or validating zone failure domains. Don't use for Cloud Storage buckets, Persistent Disk, or NetApp Volumes.

This plugin packages the [`google-cloud-filestore-auditing`](skills/google-cloud-filestore-auditing/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/google-cloud-filestore-auditing) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/google-cloud-filestore-auditing/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install google-cloud-filestore-auditing@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgoogle-cloud-filestore-auditing),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `google-cloud-filestore-auditing`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
