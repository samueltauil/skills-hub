# application-integration-basics

Explains Google Cloud Application Integration concepts, region provisioning, IAM roles, run-as service accounts, interface choices (REST, Python discovery client, Terraform, ADK), and platform limits. Use when setting up Application Integration in a Google Cloud project, enabling required APIs, provisioning a region, configuring IAM or run-as service accounts, choosing between Application Integration and custom code, or checking quotas and timeouts. Do not use for building, publishing, or invoking integrations (use application-integration-authoring) or diagnosing failed or stuck runs and logs (use application-integration-troubleshooting).

This plugin packages the [`application-integration-basics`](skills/application-integration-basics/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/application-integration-basics) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/application-integration-basics/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install application-integration-basics@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dapplication-integration-basics),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `application-integration-basics`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
