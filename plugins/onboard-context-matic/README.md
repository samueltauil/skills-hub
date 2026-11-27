# onboard-context-matic

Interactive onboarding tour for the context-matic MCP server. Walks the user through what the server does, shows all available APIs, lets them pick one to explore, explains it in their project language, demonstrates model_search and endpoint_search live, and ends with a menu of things the user can ask the agent to do. USE FOR: first-time setup; "what can this MCP do?"; "show me the available APIs"; "onboard me"; "how do I use the context-matic server"; "give me a tour". DO NOT USE FOR: actually integrating an API end-to-end (use integrate-context-matic instead).

This plugin packages the [`onboard-context-matic`](skills/onboard-context-matic/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/onboard-context-matic) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/onboard-context-matic/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install onboard-context-matic@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Donboard-context-matic),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `onboard-context-matic`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
