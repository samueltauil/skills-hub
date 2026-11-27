# iam-helper-for-privileged-access-management

Manages the end-to-end lifecycle of on-demand, temporary access using Privileged Access Manager (PAM). Use when a user asks to create, read, update, or delete PAM entitlements, request temporary access, or approve/deny pending PAM grants. Do NOT use for permanent IAM policy bindings, troubleshooting IAM permission errors, or general Google Cloud resource provisioning.

This plugin packages the [`iam-helper-for-privileged-access-management`](skills/iam-helper-for-privileged-access-management/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/iam-helper-for-privileged-access-management) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/iam-helper-for-privileged-access-management/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install iam-helper-for-privileged-access-management@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Diam-helper-for-privileged-access-management),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `iam-helper-for-privileged-access-management`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
