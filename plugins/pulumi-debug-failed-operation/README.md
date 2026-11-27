# pulumi-debug-failed-operation

Debug a Pulumi update or preview that failed: read the failure Pulumi already recorded, find what caused it, and fix it. Load this skill when the user asks to debug, diagnose, or fix a failed update or preview, or points at a failing `pulumi up` or `pulumi preview`. Don't load it for authoring new infrastructure, migrations, or provider upgrades; those have their own skills.

This plugin packages the [`pulumi-debug-failed-operation`](skills/pulumi-debug-failed-operation/SKILL.md) skill from
[pulumi/agent-skills](https://github.com/pulumi/agent-skills/tree/main/pulumi/skills/pulumi-debug-failed-operation) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/pulumi-debug-failed-operation/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install pulumi-debug-failed-operation@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpulumi-debug-failed-operation),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `pulumi-debug-failed-operation`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[pulumi/agent-skills](https://github.com/pulumi/agent-skills).
