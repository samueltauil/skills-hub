# pulumi-arm-to-pulumi

Convert or migrate Azure ARM (Azure Resource Manager) templates, Bicep templates, or code to Pulumi, including importing existing Azure resources. This skill MUST be loaded whenever a user requests migration, conversion, or import of ARM templates, Bicep templates, ARM code, Bicep code, or Azure resources to Pulumi.

This plugin packages the [`pulumi-arm-to-pulumi`](skills/pulumi-arm-to-pulumi/SKILL.md) skill from
[pulumi/agent-skills](https://github.com/pulumi/agent-skills/tree/main/migration/skills/pulumi-arm-to-pulumi) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/pulumi-arm-to-pulumi/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install pulumi-arm-to-pulumi@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpulumi-arm-to-pulumi),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `pulumi-arm-to-pulumi`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[pulumi/agent-skills](https://github.com/pulumi/agent-skills).
