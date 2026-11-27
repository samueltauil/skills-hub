# pulumi-terraform-to-pulumi

Migrate Terraform/OpenTofu projects to Pulumi, including translating HCL source code and/or importing Terraform state into a Pulumi stack. Use when a user wants to convert Terraform to Pulumi, migrate from HCL, or import tfstate into Pulumi. Do NOT trigger for general Terraform-vs-Pulumi comparisons or questions about using both tools side-by-side.

This plugin packages the [`pulumi-terraform-to-pulumi`](skills/pulumi-terraform-to-pulumi/SKILL.md) skill from
[pulumi/agent-skills](https://github.com/pulumi/agent-skills/tree/main/migration/skills/pulumi-terraform-to-pulumi) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/pulumi-terraform-to-pulumi/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install pulumi-terraform-to-pulumi@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpulumi-terraform-to-pulumi),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `pulumi-terraform-to-pulumi`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[pulumi/agent-skills](https://github.com/pulumi/agent-skills).
