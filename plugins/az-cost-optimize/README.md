# az-cost-optimize

Analyze Azure resources used in the app (IaC files and/or resources in a target rg) and optimize costs - creating GitHub issues for identified optimizations.

This plugin packages the [`az-cost-optimize`](skills/az-cost-optimize/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/az-cost-optimize) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/az-cost-optimize/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install az-cost-optimize@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Daz-cost-optimize),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `az-cost-optimize`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
