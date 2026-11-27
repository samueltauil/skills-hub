# kibana-cases

Manage investigation and incident cases across Elastic Security, Observability, and Stack Management — create, search, update, and enrich cases with comments, alerts, events, and observables (IOCs). Use when tracking incidents, correlating alerts to a case, adding investigation notes, updating status or severity, or managing triage output.

This plugin packages the [`kibana-cases`](skills/kibana-cases/SKILL.md) skill from
[elastic/agent-skills](https://github.com/elastic/agent-skills/tree/main/skills/kibana/kibana-cases) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/kibana-cases/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install kibana-cases@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dkibana-cases),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `kibana-cases`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[elastic/agent-skills](https://github.com/elastic/agent-skills).
