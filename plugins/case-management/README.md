# case-management

Create, search, update, and manage SOC cases via the Kibana Cases API. Use when tracking incidents, linking alerts to cases, adding investigation notes, or managing triage output.

This plugin packages the [`security-case-management`](skills/security-case-management/SKILL.md) skill from
[elastic/agent-skills](https://github.com/elastic/agent-skills/tree/main/skills/security/case-management) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/case-management/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install case-management@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcase-management),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `case-management`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[elastic/agent-skills](https://github.com/elastic/agent-skills).
