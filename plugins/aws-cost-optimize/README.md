# aws-cost-optimize

Analyze AWS resources used in the app (IaC files and/or resources in a target account/region) and optimize costs - creating GitHub issues for identified optimizations.

This plugin packages the [`aws-cost-optimize`](skills/aws-cost-optimize/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/aws-cost-optimize) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/aws-cost-optimize/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install aws-cost-optimize@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Daws-cost-optimize),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `aws-cost-optimize`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
