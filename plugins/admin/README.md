# admin

Manage Grafana Cloud accounts — organizations, stacks, RBAC roles and assignments, SSO/SAML/OAuth/GitHub auth, service accounts for CI/CD, user invites, team membership, and API-driven provisioning. Creates stacks via the Cloud API, mints service-account tokens, applies role assignments, configures SSO providers, and provisions teams/folders/dashboards via Terraform. Use when managing Grafana Cloud access, configuring SSO/SAML/OAuth, setting up service accounts for Terraform/CI/CD, assigning RBAC roles, inviting users, managing multiple stacks or organizations, provisioning cloud resources via API or Terraform, or auditing admin actions — even when the user says "set up SSO", "create a stack", "make a service account", or "onboard a team" without explicitly saying "admin".

This plugin packages the [`admin`](skills/admin/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-cloud/admin) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/admin/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install admin@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dadmin),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `admin`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
