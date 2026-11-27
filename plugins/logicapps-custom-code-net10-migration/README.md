# logicapps-custom-code-net10-migration

Migrate Azure Logic Apps Standard local-function custom-code projects from .NET 8 to .NET 10. Use for legacy Logic Apps custom-code workspace upgrades, project/package configuration, custom-worker settings, publication, and integrated VS Code debugging. Not for ordinary .NET applications, standalone Azure Functions, Consumption workflows, or cloud deployment.

This plugin packages the [`logicapps-custom-code-net10-migration`](skills/logicapps-custom-code-net10-migration/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/logicapps-custom-code-net10-migration) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/logicapps-custom-code-net10-migration/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install logicapps-custom-code-net10-migration@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dlogicapps-custom-code-net10-migration),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `logicapps-custom-code-net10-migration`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
