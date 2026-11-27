# pulumi-context-api

Query the Pulumi Context API, a graph query interface over an organization's infrastructure in Pulumi Cloud. Use when a question is about relationships or reachability across resources and stacks: the impact of a change ("what breaks if I change this?", blast radius), what depends on a resource or a stack's outputs, which provider instances manage which resources and at what versions, orphaned or unreferenced resources, or references that cross stacks and cloud accounts, including resources Pulumi doesn't manage. Don't load it for finding a single resource by name, type, or property (Resource Search covers that), or for update history and failure debugging (use skill `pulumi-debug-failed-operation`).

This plugin packages the [`pulumi-context-api`](skills/pulumi-context-api/SKILL.md) skill from
[pulumi/agent-skills](https://github.com/pulumi/agent-skills/tree/main/pulumi/skills/pulumi-context-api) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/pulumi-context-api/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install pulumi-context-api@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpulumi-context-api),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `pulumi-context-api`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[pulumi/agent-skills](https://github.com/pulumi/agent-skills).
