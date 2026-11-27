# spanner-graph-schema-best-practices

Designs, reviews, and optimizes physical table schemas, indexes, and graph topologies for Spanner Graph on Google Cloud. Use when creating a new Spanner Graph schema, selecting node and edge primary key types, optimizing forward, reverse, or per-node Top-K edge traversals, designing interleaved node or edge tables and covering indexes, configuring cascading deletes and row deletion policies (TTL), evaluating schematized versus schemaless dynamic label graphs, or folding 1:1 and N:1 edges into node tables. Don't use for tuning GQL query syntax or execution plans without schema changes (use spanner-graph-query-tuning), or when creating a zero-change graph overlay on existing relational tables (use spanner-relational-to-graph).

This plugin packages the [`spanner-graph-schema-best-practices`](skills/spanner-graph-schema-best-practices/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/spanner-graph-schema-best-practices) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/spanner-graph-schema-best-practices/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install spanner-graph-schema-best-practices@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dspanner-graph-schema-best-practices),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `spanner-graph-schema-best-practices`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
