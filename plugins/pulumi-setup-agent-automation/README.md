# pulumi-setup-agent-automation

Create a schedule or event trigger for an existing Pulumi Agent, or pause or resume an automation. Use when the user requests recurring or event-driven agent work, says yes to a proposed schedule or trigger, or asks to pause or resume an automation.

This plugin packages the [`pulumi-setup-agent-automation`](skills/pulumi-setup-agent-automation/SKILL.md) skill from
[pulumi/agent-skills](https://github.com/pulumi/agent-skills/tree/main/pulumi/skills/pulumi-setup-agent-automation) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/pulumi-setup-agent-automation/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install pulumi-setup-agent-automation@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpulumi-setup-agent-automation),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `pulumi-setup-agent-automation`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[pulumi/agent-skills](https://github.com/pulumi/agent-skills).
