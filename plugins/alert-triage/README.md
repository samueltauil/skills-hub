# alert-triage

Prioritize and rank the Elastic Security alert queue by weighted risk — base risk score, MITRE tactic boost, entity risk, and asset criticality — then cluster alerts into entity groups. Use when an analyst asks what to focus on, which alerts are most urgent, or wants a ranked starting point across the queue before deeper investigation begins.

This plugin packages the [`security-alert-triage`](skills/security-alert-triage/SKILL.md) skill from
[elastic/agent-skills](https://github.com/elastic/agent-skills/tree/main/skills/security/alert-triage) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/alert-triage/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install alert-triage@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dalert-triage),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `alert-triage`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[elastic/agent-skills](https://github.com/elastic/agent-skills).
