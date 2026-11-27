# skill-distribution-audit

Audit a skill collection before release or investigate installer omissions, archived/template leakage, duplicate identities, and manifest drift. Reconcile the intended public source set, distribution manifest, and actual discovery output for a specified consumer version. Includes a deterministic set-comparison helper.

This plugin packages the [`skill-distribution-audit`](skills/skill-distribution-audit/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/skill-distribution-audit) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/skill-distribution-audit/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install skill-distribution-audit@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dskill-distribution-audit),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `skill-distribution-audit`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
