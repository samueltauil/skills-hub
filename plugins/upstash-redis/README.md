# upstash-redis

Use Redis over HTTP from serverless and edge runtimes with @upstash/redis, and add rate limiting with @upstash/ratelimit. Use when the user mentions Upstash Redis, needs Redis from a Next.js route handler or middleware, Vercel, Cloudflare Workers, Deno, or Bun without TCP connection pooling, or wants cache-aside with TTLs, a session store, counters, or a 429 rate limiter using fixed window, sliding window, or token bucket. DO NOT use for self-hosted or TCP Redis clients (ioredis, node-redis), Redis Cluster administration, or vector similarity search.

This plugin packages the [`upstash-redis`](skills/upstash-redis/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/upstash-redis) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/upstash-redis/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install upstash-redis@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dupstash-redis),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `upstash-redis`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
