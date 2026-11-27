# elasticsearch-esql

Execute ES|QL (Elasticsearch Query Language) queries, use when the user wants to query Elasticsearch data, analyze logs, aggregate metrics, explore data, or create charts and dashboards from ES|QL results.

This plugin packages the [`elasticsearch-esql`](skills/elasticsearch-esql/SKILL.md) skill from
[elastic/agent-skills](https://github.com/elastic/agent-skills/tree/main/skills/elasticsearch/elasticsearch-esql) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/elasticsearch-esql/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install elasticsearch-esql@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Delasticsearch-esql),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `elasticsearch-esql`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[elastic/agent-skills](https://github.com/elastic/agent-skills).
