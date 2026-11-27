# sred-work-summary

Go back through the previous year of work and create a Notion doc that groups relevant links into projects that can then be documented as SRED projects.

This plugin packages the [`sred-work-summary`](skills/sred-work-summary/SKILL.md) skill from
[getsentry/skills](https://github.com/getsentry/skills/tree/main/skills/sred-work-summary) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/sred-work-summary/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install sred-work-summary@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsred-work-summary),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `sred-work-summary`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[getsentry/skills](https://github.com/getsentry/skills).
