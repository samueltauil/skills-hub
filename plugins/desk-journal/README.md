# desk-journal

Write, append, or read desk journal entries. The journal is persistent memory — what survives session boundaries. A good entry has: what was done, current state, next step.

This plugin packages the [`desk-journal`](skills/desk-journal/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/desk-journal) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/desk-journal/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install desk-journal@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddesk-journal),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `desk-journal`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
