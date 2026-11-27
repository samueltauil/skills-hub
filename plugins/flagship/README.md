# flagship

Build, debug, or review code that uses Cloudflare Flagship feature flags from Workers, OpenFeature SDKs, the evaluation API, or Wrangler. Use for the Flagship binding, targeting rules, percentage rollouts and A/B splits, kill switches, local flag stores, and flag-related API tokens.

This plugin packages the [`flagship`](skills/flagship/SKILL.md) skill from
[cloudflare/skills](https://github.com/cloudflare/skills/tree/main/skills/flagship) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/flagship/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install flagship@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dflagship),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `flagship`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[cloudflare/skills](https://github.com/cloudflare/skills).
