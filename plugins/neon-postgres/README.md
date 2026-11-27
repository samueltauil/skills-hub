# neon-postgres

Guides and best practices for working with Lakebase Postgres on Neon: connections, pooled vs direct, schema migrations, branching (including schema-only, reset-from-parent, and branch-per-PR workflows), autoscaling, scale-to-zero, instant restore, read replicas, IP allow lists, logical replication, egress optimization, and Lakebase Search. Use when the work is an existing DATABASE_URL, SQL, schema, inspect, or search. New backends, Auth, files, Functions, and LLM calls go to the parent `neon` skill. Live queries, reactive UIs, and realtime data go to `neon-realtime`. Also use for "@neondatabase/serverless", "@neon/neon-js", "neon inspect db", "neon postgres computes", "Neon branch", "schema-only branch", "reset branch", "branch per PR", high database bills, network transfer or egress, Free plan limits or a compute suspended over quota (SQLSTATE 53000, HTTP 402), SELECT * optimization, query overfetching, "semantic search", "vector search", "full-text search", "BM25", or "hybrid search".

This plugin packages the [`neon-postgres`](skills/neon-postgres/SKILL.md) skill from
[neondatabase/agent-skills](https://github.com/neondatabase/agent-skills/tree/main/skills/neon-postgres) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/neon-postgres/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install neon-postgres@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dneon-postgres),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `neon-postgres`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[neondatabase/agent-skills](https://github.com/neondatabase/agent-skills).
