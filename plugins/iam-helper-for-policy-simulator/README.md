# iam-helper-for-policy-simulator

Safely simulates and applies Identity and Access Management (IAM) v1 (Allow) policy changes on Google Cloud. Uses the Policy Simulator to replay historical access logs against proposed policies to prevent breaking active workloads before applying the changes. Use when simulating or applying IAM v1 allow policies across Projects, Folders, or Organizations. Don't use for analyzing IAM v2 deny policies, VPC Service Controls, or performing general policy troubleshooting.

This plugin packages the [`iam-helper-for-policy-simulator`](skills/iam-helper-for-policy-simulator/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/iam-helper-for-policy-simulator) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/iam-helper-for-policy-simulator/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install iam-helper-for-policy-simulator@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Diam-helper-for-policy-simulator),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `iam-helper-for-policy-simulator`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
