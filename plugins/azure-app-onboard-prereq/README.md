# azure-app-onboard-prereq

Assess whether source code is ready to deploy to Azure — the check BEFORE infrastructure work. Evaluates build health, app completeness, dependencies and local services, stack compatibility, and deployment feasibility. Answers questions about what your app needs before it can be deployed — frameworks, dependencies, and configuration. Checks whether dependencies are compatible and identifies deployment blockers and unsupported frameworks. WHEN: "evaluate my repo", "is my app ready to deploy", "what does my app need to deploy", "what do I need before deploying", "does my app need", "can I ship this to Azure", "scan my repo for issues", "is this app deployable", "check if my app is ready for Azure", "do I need a Dockerfile", "what's blocking my deployment", "are there any blockers", "are my dependencies compatible", "does Azure support my framework", "what needs to change before deploying", "check my app configuration".

This plugin packages the [`azure-app-onboard-prereq`](skills/azure-app-onboard-prereq/SKILL.md) skill from
[microsoft/azure-skills](https://github.com/microsoft/azure-skills/tree/main/.github/plugins/azure-skills/skills/azure-app-onboard-prereq) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/azure-app-onboard-prereq/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install azure-app-onboard-prereq@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dazure-app-onboard-prereq),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `azure-app-onboard-prereq`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[microsoft/azure-skills](https://github.com/microsoft/azure-skills).
