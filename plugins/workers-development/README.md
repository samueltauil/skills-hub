# workers-development

Run, inspect, and debug Cloudflare Workers during local development with cf dev, wrangler dev, or the Cloudflare Vite plugin, using Local Explorer to read and seed binding data and query local traces and logs. Also routes production debugging to Workers observability. Use for debugging requests whether or not the project uses Wrangler.

This plugin packages the [`workers-development`](skills/workers-development/SKILL.md) skill from
[cloudflare/skills](https://github.com/cloudflare/skills/tree/main/skills/workers-development) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/workers-development/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install workers-development@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dworkers-development),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `workers-development`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[cloudflare/skills](https://github.com/cloudflare/skills).
