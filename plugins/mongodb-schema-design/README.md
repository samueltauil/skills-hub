# mongodb-schema-design

MongoDB schema design patterns and anti-patterns. Use when designing data models, reviewing schemas, migrating from SQL, or troubleshooting performance issues caused by schema problems. Triggers on "design schema", "embed vs reference", "MongoDB data model", "schema review", "unbounded arrays", "one-to-many", "tree structure", "16MB limit", "schema validation", "JSON Schema", "time series", "schema migration", "polymorphic", "TTL", "data lifecycle", "archive", "index explosion", "unnecessary indexes", "approximation pattern", "document versioning".

This plugin packages the [`mongodb-schema-design`](skills/mongodb-schema-design/SKILL.md) skill from
[mongodb/agent-skills](https://github.com/mongodb/agent-skills/tree/main/skills/mongodb-schema-design) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/mongodb-schema-design/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install mongodb-schema-design@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmongodb-schema-design),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `mongodb-schema-design`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[mongodb/agent-skills](https://github.com/mongodb/agent-skills).
