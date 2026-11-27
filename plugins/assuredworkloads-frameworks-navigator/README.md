# assuredworkloads-frameworks-navigator

Acts as a Data Boundary Compliance Analyst that maps user compliance queries against Data Boundary Frameworks and cloud controls, validates matched resources, and recommends appropriate Frameworks or cloud controls. Use when mapping direct natural language workload requirements to Assured Workloads / Data Boundary Frameworks and cloud controls, browsing built-in Data Boundary frameworks, or identifying major requirement gaps. Don't use for non-Data-Boundary Compliance Manager posture assessments or direct Terraform deployment execution without framework selection.

This plugin packages the [`assuredworkloads-frameworks-navigator`](skills/assuredworkloads-frameworks-navigator/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/assuredworkloads-frameworks-navigator) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/assuredworkloads-frameworks-navigator/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install assuredworkloads-frameworks-navigator@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dassuredworkloads-frameworks-navigator),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `assuredworkloads-frameworks-navigator`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
