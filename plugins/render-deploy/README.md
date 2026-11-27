# render-deploy

Deploy applications to Render by analyzing codebases, generating render.yaml Blueprints, and providing Dashboard deeplinks. Use when the user wants to deploy, host, publish, or set up their application on Render's cloud platform.

This plugin packages the [`render-deploy`](skills/render-deploy/SKILL.md) skill from
[openai/skills](https://github.com/openai/skills/tree/main/skills/.curated/render-deploy) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/render-deploy/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install render-deploy@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Drender-deploy),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `render-deploy`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[openai/skills](https://github.com/openai/skills).
