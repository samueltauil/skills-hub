# what-context-needed

Ask Copilot what files it needs to see before answering a question

This plugin packages the [`what-context-needed`](skills/what-context-needed/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/what-context-needed) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/what-context-needed/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install what-context-needed@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dwhat-context-needed),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `what-context-needed`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
