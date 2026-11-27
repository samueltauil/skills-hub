# generate-security-sample-data

Generate sample security events, attack scenarios, and synthetic alerts for Elastic Security. Use when demoing, populating dashboards, testing detection rules, or setting up a POC.

This plugin packages the [`security-generate-security-sample-data`](skills/security-generate-security-sample-data/SKILL.md) skill from
[elastic/agent-skills](https://github.com/elastic/agent-skills/tree/main/skills/security/generate-security-sample-data) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/generate-security-sample-data/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install generate-security-sample-data@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgenerate-security-sample-data),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `generate-security-sample-data`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[elastic/agent-skills](https://github.com/elastic/agent-skills).
