# pulumi-create-agent

Create a reusable Pulumi Agent with saved instructions, a role, and selected integrations. Use when the user asks to create, define, or set up a new Pulumi Agent.

This plugin packages the [`pulumi-create-agent`](skills/pulumi-create-agent/SKILL.md) skill from
[pulumi/agent-skills](https://github.com/pulumi/agent-skills/tree/main/pulumi/skills/pulumi-create-agent) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/pulumi-create-agent/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install pulumi-create-agent@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpulumi-create-agent),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `pulumi-create-agent`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[pulumi/agent-skills](https://github.com/pulumi/agent-skills).
