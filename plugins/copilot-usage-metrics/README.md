# copilot-usage-metrics

Retrieve and display GitHub Copilot usage metrics for organizations and enterprises using the GitHub CLI and REST API.

This plugin packages the [`copilot-usage-metrics`](skills/copilot-usage-metrics/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/copilot-usage-metrics) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/copilot-usage-metrics/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install copilot-usage-metrics@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcopilot-usage-metrics),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `copilot-usage-metrics`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
