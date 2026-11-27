# pulumi-cdk-to-pulumi

Load this skill when a user wants to migrate, convert, port, translate, or move an AWS CDK application (including CDK stacks, constructs, or CloudFormation-synthesized templates) to Pulumi. Phrases such as "convert CDK to Pulumi", "migrate CDK app", "port CDK stacks", "replace CDK with Pulumi", "stop using CDK". Do NOT load for general CDK questions, CDK-only help, or CDK vs Pulumi comparisons where no migration is requested.

This plugin packages the [`pulumi-cdk-to-pulumi`](skills/pulumi-cdk-to-pulumi/SKILL.md) skill from
[pulumi/agent-skills](https://github.com/pulumi/agent-skills/tree/main/migration/skills/pulumi-cdk-to-pulumi) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/pulumi-cdk-to-pulumi/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install pulumi-cdk-to-pulumi@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpulumi-cdk-to-pulumi),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `pulumi-cdk-to-pulumi`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[pulumi/agent-skills](https://github.com/pulumi/agent-skills).
