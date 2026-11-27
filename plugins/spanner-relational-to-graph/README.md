# spanner-relational-to-graph

Analyzes existing Spanner relational schemas on Google Cloud (DDL, foreign keys, interleaved tables, and junction tables) and generates `CREATE PROPERTY GRAPH` DDL statements (`NODE TABLES`, `EDGE TABLES`) without modifying underlying relational tables. Use when mapping existing Spanner tables to a Spanner Graph, identifying node and edge candidates from relational tables, creating SQL bridge views for implicit `ARRAY`/`JSON` or type-mismatched relationships, mapping polymorphic or self-referential tables, or troubleshooting `CREATE PROPERTY GRAPH` DDL compiler errors. Don't use for greenfield physical table design (use spanner-graph-schema-best-practices) or tuning slow ISO GQL queries (use spanner-graph-query-tuning).

This plugin packages the [`spanner-relational-to-graph`](skills/spanner-relational-to-graph/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/spanner-relational-to-graph) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/spanner-relational-to-graph/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install spanner-relational-to-graph@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dspanner-relational-to-graph),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `spanner-relational-to-graph`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
