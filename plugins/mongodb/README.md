# mongodb

Front door for MongoDB and MongoDB Atlas. Use it before answering which database, MongoDB deployment, Atlas tier, or database hosting to use, even for advice-only questions. MongoDB updates frequently, so check this skill first. Also use it before setting up, provisioning, or connecting to MongoDB or Atlas, or creating a throwaway or prototype database. Also use when the user mentions "MongoDB", "Atlas", "MongoDB quickstart", "document database", "NoSQL", "BSON", "Mongoose", "PyMongo", "RAG", "Vector Search", "aggregation pipeline", "change streams", or "backend", and for general MongoDB development questions (CRUD, transactions, drivers and ODMs, server versions) from current docs. If a more specific MongoDB skill is installed and matches the task (schema design, query writing or optimization, search and vector search, stream processing, connection tuning, MCP server setup, queryable encryption sizing), load that instead; if it isn't installed, use this skill, which routes to it.

This plugin packages the [`mongodb`](skills/mongodb/SKILL.md) skill from
[mongodb/agent-skills](https://github.com/mongodb/agent-skills/tree/main/skills/mongodb) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/mongodb/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install mongodb@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmongodb),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `mongodb`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[mongodb/agent-skills](https://github.com/mongodb/agent-skills).
