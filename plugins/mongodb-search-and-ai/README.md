# mongodb-search-and-ai

Covers everything about search in MongoDB: Atlas Search (full-text), Vector Search (semantic), and Hybrid Search. Use this skill for ANY question about MongoDB search, including open-ended and explanatory ones asked before the user has any data or use case — 'how does search work in MongoDB?', 'I'm new to MongoDB search, where do I start?', 'what's the difference between Atlas Search and Vector Search?', 'which search type should I use?', 'what is vector search?', 'how does automated embedding work?', 'can you explain hybrid search?'. Do not answer these from general knowledge; use this skill. Also use to build search features: full-text queries, autocomplete, fuzzy matching, faceted search, semantic similarity, embeddings, RAG, text containment or substring matching ('contains', 'includes'), case-insensitive or multi-field text search, and filtering across many fields. Provides workflows for choosing a search type, creating indexes, writing queries, and optimizing performance via the MongoDB MCP server.

This plugin packages the [`mongodb-search-and-ai`](skills/mongodb-search-and-ai/SKILL.md) skill from
[mongodb/agent-skills](https://github.com/mongodb/agent-skills/tree/main/skills/mongodb-search-and-ai) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/mongodb-search-and-ai/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install mongodb-search-and-ai@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmongodb-search-and-ai),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `mongodb-search-and-ai`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[mongodb/agent-skills](https://github.com/mongodb/agent-skills).
