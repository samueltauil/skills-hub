# typespec-create-agent

Generate a complete TypeSpec declarative agent with instructions, capabilities, and conversation starters for Microsoft 365 Copilot

This plugin packages the [`typespec-create-agent`](skills/typespec-create-agent/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/typespec-create-agent) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/typespec-create-agent/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install typespec-create-agent@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dtypespec-create-agent),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `typespec-create-agent`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
