# skill-scanner

Scan agent skills for security issues. Use when asked to "scan a skill", "audit a skill", "review skill security", "check skill for injection", "validate SKILL.md", or assess whether an agent skill is safe to install. Checks for prompt injection, malicious scripts, excessive permissions, secret exposure, and supply chain risks.

This plugin packages the [`skill-scanner`](skills/skill-scanner/SKILL.md) skill from
[getsentry/skills](https://github.com/getsentry/skills/tree/main/skills/skill-scanner) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/skill-scanner/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install skill-scanner@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dskill-scanner),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `skill-scanner`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[getsentry/skills](https://github.com/getsentry/skills).
