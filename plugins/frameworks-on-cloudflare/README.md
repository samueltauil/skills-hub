# frameworks-on-cloudflare

Build, migrate, and deploy web-framework applications on Cloudflare Workers. Use when a framework project such as Astro, SvelteKit, React Router, TanStack Start, Nuxt, Hono, or a React or Vue SPA targets Cloudflare, or when a framework repository contains Workers deployment configuration.

This plugin packages the [`frameworks-on-cloudflare`](skills/frameworks-on-cloudflare/SKILL.md) skill from
[cloudflare/skills](https://github.com/cloudflare/skills/tree/main/skills/frameworks-on-cloudflare) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/frameworks-on-cloudflare/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install frameworks-on-cloudflare@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dframeworks-on-cloudflare),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `frameworks-on-cloudflare`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[cloudflare/skills](https://github.com/cloudflare/skills).
