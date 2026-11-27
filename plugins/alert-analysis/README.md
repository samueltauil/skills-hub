# alert-analysis

Investigate a specific Elastic Security detection alert: gather context, assess entity risk, classify the threat, document findings, and optionally acknowledge. Use when triaging a single known alert, performing SOC investigation, or following up after the security-alert-triage skill identifies a group to investigate.

This plugin packages the [`security-alert-analysis`](skills/security-alert-analysis/SKILL.md) skill from
[elastic/agent-skills](https://github.com/elastic/agent-skills/tree/main/skills/security/alert-analysis) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/alert-analysis/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install alert-analysis@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dalert-analysis),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `alert-analysis`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[elastic/agent-skills](https://github.com/elastic/agent-skills).
