# iam-helper-for-troubleshooting

Diagnoses, remediates, and manages Identity and Access Management (IAM) access issues on Google Cloud. Supports two distinct operational modes: (1) Requester Flow for developers encountering access denials (capturing error context, self-service PAM JIT activations, elevated developer self-remediation, or logging structured tickets), and (2) Resolver Flow for privileged administrators (authoritative Policy Troubleshooter analysis, deny policy exemptions, least-privilege role discovery, and PAM/IAM provisioning).

This plugin packages the [`iam-helper-for-troubleshooting`](skills/iam-helper-for-troubleshooting/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/iam-helper-for-troubleshooting) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/iam-helper-for-troubleshooting/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install iam-helper-for-troubleshooting@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Diam-helper-for-troubleshooting),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `iam-helper-for-troubleshooting`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
