# cloud-logging-cross-project-configuration

Configure and troubleshoot Google Cloud cross-project centralized logging and read-time aggregation. Use when: - Setting up log routing from multiple projects/folders/organizations to a central log bucket. - Creating cross-project log sinks and configuring central log buckets. - Troubleshooting cross-project routing. Don't use for single-project basic configurations.

This plugin packages the [`cloud-logging-cross-project-configuration`](skills/cloud-logging-cross-project-configuration/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/cloud-logging-cross-project-configuration) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/cloud-logging-cross-project-configuration/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install cloud-logging-cross-project-configuration@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcloud-logging-cross-project-configuration),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `cloud-logging-cross-project-configuration`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
