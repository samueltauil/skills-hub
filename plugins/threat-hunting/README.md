# threat-hunting

Hypothesis-driven threat hunting in Elastic Security using iterative ES|QL exploration. Covers IOC search, anomaly identification, baseline comparison, lateral movement tracking, and turning hunt findings into cases and detection rules. Use when running a proactive hunt, investigating suspicious activity patterns, searching for indicators of compromise, or looking for rare events in security telemetry.

This plugin packages the [`security-threat-hunting`](skills/security-threat-hunting/SKILL.md) skill from
[elastic/agent-skills](https://github.com/elastic/agent-skills/tree/main/skills/security/threat-hunting) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/threat-hunting/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install threat-hunting@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dthreat-hunting),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `threat-hunting`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[elastic/agent-skills](https://github.com/elastic/agent-skills).
