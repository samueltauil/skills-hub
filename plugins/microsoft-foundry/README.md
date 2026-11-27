# microsoft-foundry

Build, deploy, evaluate, optimize, fine-tune, and manage Microsoft Foundry agents, models, and resources end to end. USE FOR: foundry, azd ai agent, azd provision/deploy, hosted agent scaffold/develop/run/deploy/troubleshoot, prompt agent, managed harness agent, Copilot harness, voice agent, create/update/invoke/evaluate agent, add tool to agent, agent insights, batch/continuous eval, continuous monitoring, agent CI/CD, optimize/improve prompt, optimize agent instructions, Agent Optimizer, dataset curation from traces, deploy model, model fine-tuning (SFT/DPO/RFT), Foundry project, RBAC, role assignment, permissions, quota, capacity, region, deployment failure, AI Services, create Foundry resource, knowledge index, customize deployment, onboard, availability, training-data, grader, distillation, large file upload. DO NOT USE FOR: Azure Functions, App Service, general Azure deploy (use azure-deploy), general Azure prep (use azure-prepare).

This plugin packages the [`microsoft-foundry`](skills/microsoft-foundry/SKILL.md) skill from
[microsoft/azure-skills](https://github.com/microsoft/azure-skills/tree/main/.github/plugins/azure-skills/skills/microsoft-foundry) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/microsoft-foundry/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install microsoft-foundry@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmicrosoft-foundry),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `microsoft-foundry`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[microsoft/azure-skills](https://github.com/microsoft/azure-skills).
