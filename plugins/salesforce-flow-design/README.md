# salesforce-flow-design

Salesforce Flow architecture decisions, flow type selection, bulk safety validation, and fault handling standards. Use this skill when designing or reviewing Record-Triggered, Screen, Autolaunched, Scheduled, or Platform Event flows to ensure correct type selection, no DML/Get Records in loops, proper fault connectors on all data-changing elements, and appropriate automation density checks before deployment.

This plugin packages the [`salesforce-flow-design`](skills/salesforce-flow-design/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/salesforce-flow-design) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/salesforce-flow-design/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install salesforce-flow-design@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsalesforce-flow-design),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `salesforce-flow-design`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
