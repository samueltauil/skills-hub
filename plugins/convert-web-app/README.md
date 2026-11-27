# convert-web-app

This skill should be used when the user asks to "add MCP App support to my web app", "turn my web app into a hybrid MCP App", "make my web page work as an MCP App too", "wrap my existing UI as an MCP App", "convert iframe embed to MCP App", "turn my SPA into an MCP App", or needs to add MCP App support to an existing web application while keeping it working standalone. Provides guidance for analyzing existing web apps and creating a hybrid web + MCP App with server-side tool and resource registration.

This plugin packages the [`convert-web-app`](skills/convert-web-app/SKILL.md) skill from
[modelcontextprotocol/ext-apps](https://github.com/modelcontextprotocol/ext-apps/tree/main/plugins/mcp-apps/skills/convert-web-app) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/convert-web-app/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install convert-web-app@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dconvert-web-app),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `convert-web-app`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[modelcontextprotocol/ext-apps](https://github.com/modelcontextprotocol/ext-apps).
