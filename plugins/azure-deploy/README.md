# azure-deploy

Execute Azure deployments for ALREADY-PREPARED applications that have existing .azure/deployment-plan.md and infrastructure files. DO NOT use this skill when the user asks to CREATE a new application — use azure-prepare instead. This skill runs azd up, azd deploy, terraform apply, and az deployment commands with built-in error recovery. Requires .azure/deployment-plan.md from azure-prepare and validated status from azure-validate. WHEN: "run azd up", "run azd deploy", "execute deployment", "push to production", "push to cloud", "go live", "ship it", "bicep deploy", "terraform apply", "publish to Azure", "launch on Azure". DO NOT USE WHEN: "create and deploy", "build and deploy", "create a new app", "set up infrastructure", "create and deploy to Azure using Terraform" — use azure-prepare for these.

This plugin packages the [`azure-deploy`](skills/azure-deploy/SKILL.md) skill from
[microsoft/azure-skills](https://github.com/microsoft/azure-skills/tree/main/.github/plugins/azure-skills/skills/azure-deploy) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/azure-deploy/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install azure-deploy@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dazure-deploy),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `azure-deploy`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[microsoft/azure-skills](https://github.com/microsoft/azure-skills).
