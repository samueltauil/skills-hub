# pulumi-migrate-from-discovered-stack

Migrate a CloudFormation or ARM stack into a Pulumi stack, sourced from a stack that Pulumi Cloud's Discovery feature has already found and exposed via the discovered-stacks API. Load this skill when the user has a discovered stack in Pulumi Cloud and wants to bring its resources under Pulumi management. Do NOT load for greenfield Pulumi authoring, raw template conversion with no discovered-stack counterpart (i.e. no matching entry from the discovered-stacks API), or Terraform migration.

This plugin packages the [`pulumi-migrate-from-discovered-stack`](skills/pulumi-migrate-from-discovered-stack/SKILL.md) skill from
[pulumi/agent-skills](https://github.com/pulumi/agent-skills/tree/main/migration/skills/pulumi-migrate-from-discovered-stack) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/pulumi-migrate-from-discovered-stack/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install pulumi-migrate-from-discovered-stack@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpulumi-migrate-from-discovered-stack),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `pulumi-migrate-from-discovered-stack`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[pulumi/agent-skills](https://github.com/pulumi/agent-skills).
