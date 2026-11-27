# google-cloud-scc-remediation

Remediates Google Cloud Security Command Center findings, including IAM permission fixes, cloud resource misconfigurations, vulnerabilities, and Toxic Combinations. Use when asked to fix, remediate, or mitigate a Security Command Center finding or address attack paths. Don't use for general IAM policy querying without a Security Command Center finding. For runtime threat detections, this skill provides containment and investigation guidance rather than automated configuration fixes.

This plugin packages the [`google-cloud-scc-remediation`](skills/google-cloud-scc-remediation/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/google-cloud-scc-remediation) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/google-cloud-scc-remediation/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install google-cloud-scc-remediation@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgoogle-cloud-scc-remediation),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `google-cloud-scc-remediation`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
