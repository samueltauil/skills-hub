# daily-prep

Prepare for tomorrow's meetings and tasks. Pulls calendar from Outlook via WorkIQ, cross-references open tasks and workspace context, classifies meetings, detects conflicts and day-fit issues, finds learning and deep-work slots, and generates a structured HTML prep file with productivity recommendations.

This plugin packages the [`daily-prep`](skills/daily-prep/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/daily-prep) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/daily-prep/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install daily-prep@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddaily-prep),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `daily-prep`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
