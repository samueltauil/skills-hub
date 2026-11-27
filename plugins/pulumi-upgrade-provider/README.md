# pulumi-upgrade-provider

Automate Pulumi provider repo upgrades with the `upgrade-provider` tool. Use when upgrading a pulumi provider repository to a new upstream version, running `upgrade-provider`, and addressing its common failure modes like patch conflicts or missing module mappings.

This plugin packages the [`pulumi-upgrade-provider`](skills/pulumi-upgrade-provider/SKILL.md) skill from
[pulumi/agent-skills](https://github.com/pulumi/agent-skills/tree/main/package-maintenance/skills/pulumi-upgrade-provider) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/pulumi-upgrade-provider/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install pulumi-upgrade-provider@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpulumi-upgrade-provider),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `pulumi-upgrade-provider`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[pulumi/agent-skills](https://github.com/pulumi/agent-skills).
