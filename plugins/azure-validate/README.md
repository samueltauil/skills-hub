# azure-validate

Pre-deployment validation for Azure readiness. Run deep checks on configuration, infrastructure (Bicep or Terraform), RBAC role assignments, managed identity permissions, and prerequisites before deploying. WHEN: validate my app, check deployment readiness, run preflight checks, verify configuration, check if ready to deploy, validate azure.yaml, validate Bicep, test before deploying, troubleshoot deployment errors, validate Azure Functions, validate function app, validate serverless deployment, verify RBAC roles, check role assignments, review managed identity permissions, what-if analysis, validate Container Apps deployment.

This plugin packages the [`azure-validate`](skills/azure-validate/SKILL.md) skill from
[microsoft/azure-skills](https://github.com/microsoft/azure-skills/tree/main/.github/plugins/azure-skills/skills/azure-validate) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/azure-validate/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install azure-validate@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dazure-validate),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `azure-validate`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[microsoft/azure-skills](https://github.com/microsoft/azure-skills).
