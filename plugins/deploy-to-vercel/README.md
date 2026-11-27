# deploy-to-vercel

Deploy applications and websites to Vercel. Use when the user requests deployment actions like "deploy my app", "deploy and give me the link", "push this live", or "create a preview deployment".

This plugin packages the [`deploy-to-vercel`](skills/deploy-to-vercel/SKILL.md) skill from
[vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills/tree/main/skills/deploy-to-vercel) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/deploy-to-vercel/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install deploy-to-vercel@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddeploy-to-vercel),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `deploy-to-vercel`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills).
