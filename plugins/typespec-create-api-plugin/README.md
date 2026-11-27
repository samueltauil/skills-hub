# typespec-create-api-plugin

Generate a TypeSpec API plugin with REST operations, authentication, and Adaptive Cards for Microsoft 365 Copilot

This plugin packages the [`typespec-create-api-plugin`](skills/typespec-create-api-plugin/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/typespec-create-api-plugin) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/typespec-create-api-plugin/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install typespec-create-api-plugin@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dtypespec-create-api-plugin),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `typespec-create-api-plugin`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
