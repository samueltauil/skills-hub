# application-integration-authoring

Builds, versions, publishes, tests, and executes Google Cloud Application Integration workflows through the REST API and Python discovery client, and promotes versions across environments. Use when listing integrations, downloading or uploading integration versions as JSON, configuring API triggers or config variables, publishing drafts, invoking integrations, or automating CI/CD promotion. Do not use for initial region provisioning and IAM setup (use application-integration-basics) or diagnosing failed runs and logs (use application-integration-troubleshooting).

This plugin packages the [`application-integration-authoring`](skills/application-integration-authoring/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/application-integration-authoring) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/application-integration-authoring/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install application-integration-authoring@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dapplication-integration-authoring),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `application-integration-authoring`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
