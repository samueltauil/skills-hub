# elasticsearch-index-design

Design and review Elasticsearch index mappings for stated access patterns: correct field types, text+keyword multi-fields, doc_values tuning, mapping-explosion avoidance, and explicit shard settings. Use when creating a new index, reviewing a mapping for storage or query performance, fixing wrong field types, or when the user asks which type to use for search, filter, sort, or aggregation on a field.

This plugin packages the [`elasticsearch-index-design`](skills/elasticsearch-index-design/SKILL.md) skill from
[elastic/agent-skills](https://github.com/elastic/agent-skills/tree/main/skills/elasticsearch/elasticsearch-index-design) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/elasticsearch-index-design/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install elasticsearch-index-design@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Delasticsearch-index-design),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `elasticsearch-index-design`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[elastic/agent-skills](https://github.com/elastic/agent-skills).
