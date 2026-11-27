# vercel-optimize

Use for Vercel cost and performance optimization on deployed projects, especially Next.js, SvelteKit, Nuxt, and limited Astro apps. Collect Vercel metrics, usage, project config, and code scan results first; investigate only metric-backed candidates; produce ranked recommendations grounded in verified files and version-aware Vercel/framework docs. Trigger for Vercel bill reduction, slow or expensive routes, caching opportunities, Function Invocations, Build Minutes, Fast Data Transfer, Core Web Vitals, Bot Management, Fluid compute, or cost breakdown requests.

This plugin packages the [`vercel-optimize`](skills/vercel-optimize/SKILL.md) skill from
[vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills/tree/main/skills/vercel-optimize) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/vercel-optimize/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install vercel-optimize@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dvercel-optimize),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `vercel-optimize`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills).
