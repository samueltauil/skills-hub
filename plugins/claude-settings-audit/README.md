# claude-settings-audit

Analyze a repository to generate recommended Claude Code settings.json permissions. Use when setting up a new project, auditing existing settings, or determining which read-only bash commands to allow. Detects tech stack, build tools, and monorepo structure.

This plugin packages the [`claude-settings-audit`](skills/claude-settings-audit/SKILL.md) skill from
[getsentry/skills](https://github.com/getsentry/skills/tree/main/skills/claude-settings-audit) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/claude-settings-audit/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install claude-settings-audit@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dclaude-settings-audit),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `claude-settings-audit`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[getsentry/skills](https://github.com/getsentry/skills).
