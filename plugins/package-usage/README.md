# package-usage

Track which stacks across a Pulumi organization use a specific package and at what versions. Use for cross-stack audits, identifying outdated or unmaintained package versions across many stacks, finding affected stacks before publishing breaking changes to a component package, or planning coordinated upgrade rollouts. Do NOT use for upgrading a cloud provider package (pulumi-aws, pulumi-azure-native, pulumi-gcp, pulumi-kubernetes, etc.) in a single project — use skill `provider-upgrade` instead. Do NOT use for general infrastructure creation, resource provisioning, or how-to questions about a package.

This plugin packages the [`package-usage`](skills/package-usage/SKILL.md) skill from
[pulumi/agent-skills](https://github.com/pulumi/agent-skills/tree/main/pulumi/skills/package-usage) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/package-usage/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install package-usage@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpackage-usage),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `package-usage`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[pulumi/agent-skills](https://github.com/pulumi/agent-skills).
