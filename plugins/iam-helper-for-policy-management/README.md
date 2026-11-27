# iam-helper-for-policy-management

Streamlines the creation, modification, and management of IAM allow policies (v1) and deny policies (v2). Manages access control across Resource Manager resources (Organization, Folder, Project) and individual resources. Use when creating, updating, listing, or deleting IAM allow policies or deny policies. Don't use for access denial troubleshooting (use iam-helper-for-troubleshooting), temporary privileged access (use iam-helper-for-privileged-access-management), configuring VPC Service Controls, or managing network firewall rules.

This plugin packages the [`iam-helper-for-policy-management`](skills/iam-helper-for-policy-management/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/iam-helper-for-policy-management) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/iam-helper-for-policy-management/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install iam-helper-for-policy-management@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Diam-helper-for-policy-management),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `iam-helper-for-policy-management`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
