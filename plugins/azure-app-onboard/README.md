# azure-app-onboard

End-to-end orchestrator: from a business idea, app idea, or existing app to running Azure deployment with cost estimates and pre-deploy approval. Analyzes your app, auto-detects the right Azure services, scaffolds infrastructure code, and deploys — tailored to your app, not a template. Handles moving existing apps to Azure without rewriting or with minimal changes. WHEN: bring your app to Azure, plan my app, cost to run, is my code ready to deploy, deploy my app to the cloud, deploy all my services, what Azure services do I need, plan my Azure deployment, deploy my new app to Azure, one-click deploy, I have an app and want it on Azure, migrate my app to Azure, help me get started, build an app, no code yet, starter project. DO NOT USE FOR: use azd for deployment(use azure-deploy), optimizing existing costs (use cost-optimization), code readiness checks only (use azure-app-onboard-prereq).

This plugin packages the [`azure-app-onboard`](skills/azure-app-onboard/SKILL.md) skill from
[microsoft/azure-skills](https://github.com/microsoft/azure-skills/tree/main/.github/plugins/azure-skills/skills/azure-app-onboard) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/azure-app-onboard/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install azure-app-onboard@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dazure-app-onboard),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `azure-app-onboard`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[microsoft/azure-skills](https://github.com/microsoft/azure-skills).
