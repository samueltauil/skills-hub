# assured-workloads-basics

Provisions, inspects, updates, and deletes Google Cloud Assured Workloads V1 compliant folders, CMEK settings, Sovereign Controls by Partners, and service usage restrictions. Use when creating, listing, describing, updating, or deleting an Assured Workloads workload for any compliance regime or data boundary (FedRAMP, DoD IL2/IL4/IL5, ITAR, CJIS, Healthcare, Sovereign Controls by Partners, or Regional Data Boundaries). Don't use for brownfield assessments or custom frameworks (use assuredworkloads-environment-assessor or assuredworkloads-frameworks-*), or non-compliant folders.

This plugin packages the [`assured-workloads-basics`](skills/assured-workloads-basics/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/assured-workloads-basics) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/assured-workloads-basics/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install assured-workloads-basics@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dassured-workloads-basics),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `assured-workloads-basics`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
