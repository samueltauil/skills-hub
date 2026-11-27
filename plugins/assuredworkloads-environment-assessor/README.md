# assuredworkloads-environment-assessor

Discover Google Cloud resource telemetry and effective Org Policies, evaluate brownfield workloads against sovereign data boundary and compliance standards (EU Data Boundary with Support, FedRAMP Moderate/High, DoD IL4/IL5, ITAR, CJIS, US/EU Regional Data Boundaries), and recommend the optimal Assured Workloads Framework. Use when asked to: "assess my environment for compliance", "which Assured Workloads framework should I use?", "check if my folder is ready for EU sovereignty", "evaluate compliance posture for folders/123 or projects/xyz", or "discover compliance gaps before deployment". Do NOT use for live mutating policy deployments, generating deep audit reports via Cloud Audit Manager, generating remediation scripts, or authoring custom Assured Workloads frameworks.

This plugin packages the [`assuredworkloads-environment-assessor`](skills/assuredworkloads-environment-assessor/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/assuredworkloads-environment-assessor) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/assuredworkloads-environment-assessor/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install assuredworkloads-environment-assessor@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dassuredworkloads-environment-assessor),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `assuredworkloads-environment-assessor`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
