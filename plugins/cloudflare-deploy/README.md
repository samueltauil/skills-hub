# cloudflare-deploy

Deploy applications and infrastructure to Cloudflare using Workers, Pages, and related platform services. Use when the user asks to deploy, host, publish, or set up a project on Cloudflare.

This plugin packages the [`cloudflare-deploy`](skills/cloudflare-deploy/SKILL.md) skill from
[openai/skills](https://github.com/openai/skills/tree/main/skills/.curated/cloudflare-deploy) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/cloudflare-deploy/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install cloudflare-deploy@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcloudflare-deploy),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `cloudflare-deploy`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[openai/skills](https://github.com/openai/skills).
