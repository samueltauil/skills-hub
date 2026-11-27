# msgraph-sdk

Integrate Microsoft Graph SDK into any project — .NET, TypeScript/JavaScript, or Python. Covers auth patterns (client credentials, OBO, managed identity), SDK setup, calling Graph APIs, batching, delta queries, change notifications, throttling, and permission scopes. Use when accessing Microsoft 365 data (users, mail, calendar, Teams, files, SharePoint) from any application type.

This plugin packages the [`msgraph-sdk`](skills/msgraph-sdk/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/msgraph-sdk) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/msgraph-sdk/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install msgraph-sdk@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmsgraph-sdk),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `msgraph-sdk`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
