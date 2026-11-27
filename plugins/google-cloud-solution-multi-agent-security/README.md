# google-cloud-solution-multi-agent-security

Designs, deploys, and secures Google Cloud Agent Gateway solutions. Use when the user needs to configure multi-agent security, ingress (CLIENT_TO_AGENT), or egress (AGENT_TO_ANYWHERE) patterns involving Model Armor, IAP, and Agent Registry. Don't use for general Cloud Load Balancing or basic VPC setup not related to Agent Gateways.

This plugin packages the [`google-cloud-solution-multi-agent-security`](skills/google-cloud-solution-multi-agent-security/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/google-cloud-solution-multi-agent-security) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/google-cloud-solution-multi-agent-security/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install google-cloud-solution-multi-agent-security@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgoogle-cloud-solution-multi-agent-security),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `google-cloud-solution-multi-agent-security`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
