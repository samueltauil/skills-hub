# kibana-alerting-rules

Create and manage Kibana alerting rules and the action policies that notify on their alerts, for both Universal Alerting and classic alerting. Use when the user wants to be alerted or notified about conditions in their data, change where or how often alerts notify (including snoozing notifications), edit, enable, disable, or delete existing rules or action policies, or list existing alerting, including managing rules with Terraform. Not for Security detection rules.

This plugin packages the [`kibana-alerting-rules`](skills/kibana-alerting-rules/SKILL.md) skill from
[elastic/agent-skills](https://github.com/elastic/agent-skills/tree/main/skills/kibana/kibana-alerting-rules) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/kibana-alerting-rules/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install kibana-alerting-rules@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dkibana-alerting-rules),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `kibana-alerting-rules`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[elastic/agent-skills](https://github.com/elastic/agent-skills).
