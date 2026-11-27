# workers-profiling

Profile or debug CPU usage and memory allocation in deployed Cloudflare Workers and Durable Objects. Then use this information to optimize your code.

This plugin packages the [`workers-profiling`](skills/workers-profiling/SKILL.md) skill from
[cloudflare/skills](https://github.com/cloudflare/skills/tree/main/skills/workers-profiling) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/workers-profiling/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install workers-profiling@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dworkers-profiling),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `workers-profiling`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[cloudflare/skills](https://github.com/cloudflare/skills).
