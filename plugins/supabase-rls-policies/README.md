# supabase-rls-policies

Write, review, and test Supabase Row Level Security (RLS) policies so that one user cannot read or change another user's rows. Use when creating or changing tables, policies, views, or security definer functions in a Supabase project, when reviewing a migration that touches RLS, or when asked to prove user isolation with pgTAP tests that sign in as two users.

This plugin packages the [`supabase-rls-policies`](skills/supabase-rls-policies/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/supabase-rls-policies) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/supabase-rls-policies/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install supabase-rls-policies@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsupabase-rls-policies),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `supabase-rls-policies`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
