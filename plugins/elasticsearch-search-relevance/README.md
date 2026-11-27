# elasticsearch-search-relevance

Improve Elasticsearch search relevance for content and catalog indices: pin or promote results with query rules (correct rule type, criteria, and rule-query wiring) and tune organic ranking with multi_match, field boosts, and analysis grounded in the index mapping. Use when search results rank poorly, a specific document must appear first for a query, or the user asks to tune full-text matching — not for ES|QL analytics, index ingest, or cluster health.

This plugin packages the [`elasticsearch-search-relevance`](skills/elasticsearch-search-relevance/SKILL.md) skill from
[elastic/agent-skills](https://github.com/elastic/agent-skills/tree/main/skills/elasticsearch/elasticsearch-search-relevance) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/elasticsearch-search-relevance/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install elasticsearch-search-relevance@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Delasticsearch-search-relevance),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `elasticsearch-search-relevance`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[elastic/agent-skills](https://github.com/elastic/agent-skills).
