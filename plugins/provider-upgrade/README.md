# provider-upgrade

Upgrade any Pulumi provider to a newer version and reconcile the resulting diff. Use when users want to upgrade or update a provider (including editing package.json, requirements.txt, pyproject.toml, go.mod, or Pulumi.yaml to bump a provider SDK), check for breaking changes before or during an upgrade, fix resources that broke after a provider upgrade, or resolve unexpected replacements, creates, or deletes in a post-upgrade preview, including pulumi-gcp v10 errors such as a missing gcp.notebooks or gcp.iap.Brand type or a required secretDataWoVersion. Applies to all providers (aws, azure-native, gcp, kubernetes, aws-native, cloudflare, datadog, etc.) — not just Tier 1. Do NOT use for querying which stacks use what package versions; use skill `package-usage` for cross-stack audits. Do NOT use for general infrastructure tasks.

This plugin packages the [`provider-upgrade`](skills/provider-upgrade/SKILL.md) skill from
[pulumi/agent-skills](https://github.com/pulumi/agent-skills/tree/main/pulumi/skills/provider-upgrade) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/provider-upgrade/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install provider-upgrade@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dprovider-upgrade),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `provider-upgrade`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[pulumi/agent-skills](https://github.com/pulumi/agent-skills).
