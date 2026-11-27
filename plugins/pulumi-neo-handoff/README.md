# pulumi-neo-handoff

Hand off the current thread to a new Pulumi Neo task as a one-way transfer. Use when the user explicitly asks to hand off, send, transfer, or continue current work in Pulumi Neo (e.g. "hand this to Neo", "continue in Neo", "/neo-handoff"). Do not load when the user only mentions Neo, asks what Neo can do, asks for an AI-written PR or preview explanation, or hands off to a different agent.

This plugin packages the [`pulumi-neo-handoff`](skills/pulumi-neo-handoff/SKILL.md) skill from
[pulumi/agent-skills](https://github.com/pulumi/agent-skills/tree/main/delegation/skills/pulumi-neo-handoff) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/pulumi-neo-handoff/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install pulumi-neo-handoff@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpulumi-neo-handoff),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `pulumi-neo-handoff`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[pulumi/agent-skills](https://github.com/pulumi/agent-skills).
