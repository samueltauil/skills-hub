# detection-rule-management

Create, tune, and manage Elastic Security detection rules (SIEM and Endpoint). Use for false positives, exceptions, new coverage, noisy rules, or rule management via Kibana API.

This plugin packages the [`security-detection-rule-management`](skills/security-detection-rule-management/SKILL.md) skill from
[elastic/agent-skills](https://github.com/elastic/agent-skills/tree/main/skills/security/detection-rule-management) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/detection-rule-management/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install detection-rule-management@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddetection-rule-management),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `detection-rule-management`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[elastic/agent-skills](https://github.com/elastic/agent-skills).
