# mongodb-natural-language-querying

Generate read-only MongoDB queries (find) or aggregation pipelines using natural language, with collection schema context and sample documents. Use this skill whenever the user asks to write, create, or generate MongoDB queries, wants to filter/query/aggregate data in MongoDB, asks "how do I query...", needs help with query syntax, or discusses finding/filtering/grouping MongoDB documents. Also use for translating SQL-like requests to MongoDB syntax. Does NOT handle Atlas Search ($search operator), vector/semantic search ($vectorSearch operator), fuzzy matching, autocomplete indexes, or relevance scoring - use search-and-ai for those. Does NOT analyze or optimize existing queries - use mongodb-query-optimizer for that. Does NOT handle aggregation pipelines that involve write operations. Requires MongoDB MCP server.

This plugin packages the [`mongodb-natural-language-querying`](skills/mongodb-natural-language-querying/SKILL.md) skill from
[mongodb/agent-skills](https://github.com/mongodb/agent-skills/tree/main/skills/mongodb-natural-language-querying) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/mongodb-natural-language-querying/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install mongodb-natural-language-querying@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmongodb-natural-language-querying),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `mongodb-natural-language-querying`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[mongodb/agent-skills](https://github.com/mongodb/agent-skills).
