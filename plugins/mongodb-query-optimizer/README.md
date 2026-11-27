# mongodb-query-optimizer

Help with MongoDB query optimization and indexing. Use only when the user asks for optimization or performance: "How do I optimize this query?", "How do I index this?", "Why is this query slow?", "Can you fix my slow queries?", "What are the slow queries on my cluster?", etc. Do not invoke for general MongoDB query writing unless user asks for performance or index help. Prefer indexing as optimization strategy. Use MongoDB MCP when available.

This plugin packages the [`mongodb-query-optimizer`](skills/mongodb-query-optimizer/SKILL.md) skill from
[mongodb/agent-skills](https://github.com/mongodb/agent-skills/tree/main/skills/mongodb-query-optimizer) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/mongodb-query-optimizer/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install mongodb-query-optimizer@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmongodb-query-optimizer),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `mongodb-query-optimizer`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[mongodb/agent-skills](https://github.com/mongodb/agent-skills).
