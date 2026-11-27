# elasticsearch-query-optimization

Diagnose slow Elasticsearch Query DSL searches and propose measured fixes. Use when a search is slow, profile output shows an expensive clause, exact-match filters sit in scoring context, or leading wildcards dominate latency. Ground every recommendation in search profiling — move non-scoring clauses to filter context, eliminate leading wildcards, and re-profile to confirm improvement.

This plugin packages the [`elasticsearch-query-optimization`](skills/elasticsearch-query-optimization/SKILL.md) skill from
[elastic/agent-skills](https://github.com/elastic/agent-skills/tree/main/skills/elasticsearch/elasticsearch-query-optimization) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/elasticsearch-query-optimization/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install elasticsearch-query-optimization@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Delasticsearch-query-optimization),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `elasticsearch-query-optimization`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[elastic/agent-skills](https://github.com/elastic/agent-skills).
