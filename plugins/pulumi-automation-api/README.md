# pulumi-automation-api

Load this skill when a user asks how to run Pulumi programmatically, embed Pulumi in an application, orchestrate multiple stacks in code, build a self-service infrastructure portal, replace pulumi CLI shell scripts with code, or use the Pulumi Automation API (LocalWorkspace, createOrSelectStack, inline programs). Also load for questions about multi-stack sequencing, parallel deployments, or passing outputs between stacks via code.

This plugin packages the [`pulumi-automation-api`](skills/pulumi-automation-api/SKILL.md) skill from
[pulumi/agent-skills](https://github.com/pulumi/agent-skills/tree/main/pulumi/skills/pulumi-automation-api) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/pulumi-automation-api/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install pulumi-automation-api@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpulumi-automation-api),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `pulumi-automation-api`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[pulumi/agent-skills](https://github.com/pulumi/agent-skills).
