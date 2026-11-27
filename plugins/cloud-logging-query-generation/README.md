# cloud-logging-query-generation

Generates Logging Query Language (LQL) queries for Cloud Logging on Google Cloud from natural language. Use this skill when you need to query log data or when you are debugging issues. You can filter log data by Google Cloud service. Don't use this skill to query other databases, such as SQL or Cloud Spanner.

This plugin packages the [`cloud-logging-query-generation`](skills/cloud-logging-query-generation/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/cloud-logging-query-generation) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/cloud-logging-query-generation/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install cloud-logging-query-generation@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcloud-logging-query-generation),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `cloud-logging-query-generation`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
