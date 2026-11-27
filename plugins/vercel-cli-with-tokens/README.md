# vercel-cli-with-tokens

Deploy and manage projects on Vercel using token-based authentication. Use when working with Vercel CLI using access tokens rather than interactive login — e.g. "deploy to vercel", "set up vercel", "add environment variables to vercel".

This plugin packages the [`vercel-cli-with-tokens`](skills/vercel-cli-with-tokens/SKILL.md) skill from
[vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills/tree/main/skills/vercel-cli-with-tokens) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/vercel-cli-with-tokens/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install vercel-cli-with-tokens@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dvercel-cli-with-tokens),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `vercel-cli-with-tokens`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills).
