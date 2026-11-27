# cloudformation-to-pulumi

Convert, migrate, or import AWS CloudFormation stacks or templates into Pulumi programs. Load this skill whenever a user wants to move from CloudFormation to Pulumi, convert a CFN template, import existing CloudFormation-managed resources into Pulumi, or asks about CloudFormation-to-Pulumi migration in any form. Also load when the user mentions cdk-importer in a migration context.

This plugin packages the [`cloudformation-to-pulumi`](skills/cloudformation-to-pulumi/SKILL.md) skill from
[pulumi/agent-skills](https://github.com/pulumi/agent-skills/tree/main/migration/skills/cloudformation-to-pulumi) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/cloudformation-to-pulumi/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install cloudformation-to-pulumi@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcloudformation-to-pulumi),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `cloudformation-to-pulumi`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[pulumi/agent-skills](https://github.com/pulumi/agent-skills).
