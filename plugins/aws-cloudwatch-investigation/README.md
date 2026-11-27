# aws-cloudwatch-investigation

Reusable investigation patterns for AWS CloudWatch: Logs Insights query templates, alarm-to-deployment correlation, blast-radius narrowing decision tree, and PromQL-style metric query patterns for structured incident triage.

This plugin packages the [`aws-cloudwatch-investigation`](skills/aws-cloudwatch-investigation/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/aws-cloudwatch-investigation) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/aws-cloudwatch-investigation/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install aws-cloudwatch-investigation@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Daws-cloudwatch-investigation),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `aws-cloudwatch-investigation`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
