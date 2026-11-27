# netlify-deploy

Deploy web projects to Netlify using the Netlify CLI (`npx netlify`). Use when the user asks to deploy, host, publish, or link a site/repo on Netlify, including preview and production deploys.

This plugin packages the [`netlify-deploy`](skills/netlify-deploy/SKILL.md) skill from
[openai/skills](https://github.com/openai/skills/tree/main/skills/.curated/netlify-deploy) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/netlify-deploy/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install netlify-deploy@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dnetlify-deploy),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `netlify-deploy`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[openai/skills](https://github.com/openai/skills).
