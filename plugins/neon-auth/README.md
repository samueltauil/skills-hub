# neon-auth

Add authentication to a new app. Use for "add auth", "add login", Neon Auth (Managed Better Auth), identity routing, sign-up, sign-in, password reset, email OTP, magic links, organizations, phone OTP, OAuth, OAuth server for MCP or third-party OAuth clients, passkeys, MFA, trusted domains, invalid domain, and @neon/auth. No existing identity: default to Managed Better Auth. Keep working Better Auth, Clerk, Supabase Auth, or another IdP. User asked to migrate from Supabase Auth: Managed Better Auth. A required plugin outside Managed support: self-managed Better Auth on a Neon Function or the existing app host. Also use for auth APIs in @neon/neon-js.

This plugin packages the [`neon-auth`](skills/neon-auth/SKILL.md) skill from
[neondatabase/agent-skills](https://github.com/neondatabase/agent-skills/tree/main/skills/neon-auth) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/neon-auth/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install neon-auth@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dneon-auth),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `neon-auth`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[neondatabase/agent-skills](https://github.com/neondatabase/agent-skills).
