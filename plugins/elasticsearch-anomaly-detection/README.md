# elasticsearch-anomaly-detection

Create and manage Elastic ML anomaly detection jobs via the API. Use when setting up jobs on an index or data stream, configuring jobs and datafeeds, or opening, starting, or stopping them.

This plugin packages the [`elasticsearch-anomaly-detection`](skills/elasticsearch-anomaly-detection/SKILL.md) skill from
[elastic/agent-skills](https://github.com/elastic/agent-skills/tree/main/skills/elasticsearch/elasticsearch-anomaly-detection) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/elasticsearch-anomaly-detection/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install elasticsearch-anomaly-detection@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Delasticsearch-anomaly-detection),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `elasticsearch-anomaly-detection`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[elastic/agent-skills](https://github.com/elastic/agent-skills).
