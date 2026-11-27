# pulumi-best-practices

Load when the user is writing, reviewing, or debugging Pulumi TypeScript/Python programs; asks about Output<T> or apply() usage; wants to create ComponentResource classes; needs to refactor resources without destroying them (aliases); is setting up secrets or config; or is configuring a pulumi preview/up CI workflow. Also load for questions about resource dependency order, parent/child resource relationships, or pulumi.interpolate.

This plugin packages the [`pulumi-best-practices`](skills/pulumi-best-practices/SKILL.md) skill from
[pulumi/agent-skills](https://github.com/pulumi/agent-skills/tree/main/pulumi/skills/pulumi-best-practices) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/pulumi-best-practices/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install pulumi-best-practices@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpulumi-best-practices),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `pulumi-best-practices`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[pulumi/agent-skills](https://github.com/pulumi/agent-skills).
