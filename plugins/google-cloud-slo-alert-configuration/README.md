# google-cloud-slo-alert-configuration

Configures Cloud Monitoring PromQL-based Service Level Objective (SLO) alerting policies on Google Cloud for resources registered in App Hub or individually specified. Generates Terraform output. Use when the user asks to configure an SLO or Service Level Objective. Don't use for standard alerting policies.

This plugin packages the [`google-cloud-slo-alert-configuration`](skills/google-cloud-slo-alert-configuration/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/google-cloud-slo-alert-configuration) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/google-cloud-slo-alert-configuration/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install google-cloud-slo-alert-configuration@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgoogle-cloud-slo-alert-configuration),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `google-cloud-slo-alert-configuration`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
