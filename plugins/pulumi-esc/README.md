# pulumi-esc

Guidance for working with Pulumi ESC (Environments, Secrets, and Configuration). Use when users ask about managing secrets, configuration, environments, short-term credentials, configuring OIDC for AWS, Azure, GCP, integrating with secret stores (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault, 1Password), or using ESC with Pulumi stacks.

This plugin packages the [`pulumi-esc`](skills/pulumi-esc/SKILL.md) skill from
[pulumi/agent-skills](https://github.com/pulumi/agent-skills/tree/main/pulumi/skills/pulumi-esc) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/pulumi-esc/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install pulumi-esc@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpulumi-esc),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `pulumi-esc`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[pulumi/agent-skills](https://github.com/pulumi/agent-skills).
