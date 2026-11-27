# elasticsearch-ingest

Load local CSV, JSON array, and NDJSON files into Elasticsearch indices with the bulk API through the `elastic` CLI, creating an explicit mapping first when field types matter. Use when batch-importing local files, loading a pre-formed bulk NDJSON body, or verifying document counts and mappings after a load — not for Logstash pipelines, Beats, Elastic Agent, continuous ingestion, or index-to-index reindex.

This plugin packages the [`elasticsearch-ingest`](skills/elasticsearch-ingest/SKILL.md) skill from
[elastic/agent-skills](https://github.com/elastic/agent-skills/tree/main/skills/elasticsearch/elasticsearch-ingest) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/elasticsearch-ingest/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install elasticsearch-ingest@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Delasticsearch-ingest),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `elasticsearch-ingest`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[elastic/agent-skills](https://github.com/elastic/agent-skills).
