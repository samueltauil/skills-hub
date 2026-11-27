# pulumi-component

Guide for authoring Pulumi ComponentResource classes. Use when creating reusable infrastructure components, designing component interfaces, setting up multi-language support, or distributing component packages.

This plugin packages the [`pulumi-component`](skills/pulumi-component/SKILL.md) skill from
[pulumi/agent-skills](https://github.com/pulumi/agent-skills/tree/main/pulumi/skills/pulumi-component) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/pulumi-component/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install pulumi-component@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpulumi-component),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `pulumi-component`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[pulumi/agent-skills](https://github.com/pulumi/agent-skills).
