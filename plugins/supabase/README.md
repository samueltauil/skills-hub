# supabase

Use when doing ANY task involving Supabase. Triggers: Supabase products (Database, Auth, Edge Functions, Realtime, Storage, Vectors, Cron, Queues); client libraries and SSR integrations (supabase-js, @supabase/ssr) in Next.js, React, SvelteKit, Astro, Remix; auth issues (login, logout, sessions, JWT, cookies, getSession, getUser, getClaims, RLS); Supabase CLI or MCP server; schema changes, migrations, declarative schemas, security audits, Postgres extensions (pg_graphql, pg_cron, pg_vector); debugging and troubleshooting errors or unexpected behavior on Supabase projects (HTTP errors, Postgres errors, RLS surprises, permission denied, schema cache issues, timeouts, Edge Function crashes, Realtime drops, Storage failures) and reading or querying logs (Logs Explorer, ClickHouse).

This plugin packages the [`supabase`](skills/supabase/SKILL.md) skill from
[supabase/agent-skills](https://github.com/supabase/agent-skills/tree/main/skills/supabase) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/supabase/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install supabase@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsupabase),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `supabase`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[supabase/agent-skills](https://github.com/supabase/agent-skills).
