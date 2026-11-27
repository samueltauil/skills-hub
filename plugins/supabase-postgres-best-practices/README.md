# supabase-postgres-best-practices

Postgres best practices maintained by Supabase, for Postgres running anywhere. Load this skill BEFORE writing or changing anything that lives in a Postgres database: creating or altering tables and columns (including choosing column types), schema design, migrations and declarative schema files, RLS policies and the tests that verify them, indexes, triggers, database functions, queues and scheduled jobs (pg_cron, pgmq), vector/semantic search (pgvector), and restoring dumps (pg_restore) or importing data. Also load it when diagnosing slow queries, high CPU, timeouts, EXPLAIN plans, connection exhaustion, locking, bloat, or rows visible to the wrong user or tenant. This is not just a performance guide — schema, migration, security, and SQL authoring tasks need these rules too, even for a one-column change or a single query.

This plugin packages the [`supabase-postgres-best-practices`](skills/supabase-postgres-best-practices/SKILL.md) skill from
[supabase/agent-skills](https://github.com/supabase/agent-skills/tree/main/skills/supabase-postgres-best-practices) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/supabase-postgres-best-practices/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install supabase-postgres-best-practices@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsupabase-postgres-best-practices),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `supabase-postgres-best-practices`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[supabase/agent-skills](https://github.com/supabase/agent-skills).
