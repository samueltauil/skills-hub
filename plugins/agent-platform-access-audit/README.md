# agent-platform-access-audit

Audits AI agent data access, blast radius, and blocked policy operations in Google Cloud by querying Cloud Audit Logs via BigQuery. Use when investigating what resources or services an agent accessed, identifying top originating principals the agent is acting as, or triaging PERMISSION_DENIED errors to distinguish VPC Service Controls perimeter violations from IAM permission denials. Don't use for configuring Cloud Monitoring alert policies, modifying IAM policies or VPC Service Controls perimeters, querying non-audit application logs, or performing write operations.

This plugin packages the [`agent-platform-access-audit`](skills/agent-platform-access-audit/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/agent-platform-access-audit) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/agent-platform-access-audit/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install agent-platform-access-audit@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dagent-platform-access-audit),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `agent-platform-access-audit`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
