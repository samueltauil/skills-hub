# java-mcp-server-generator

Use this skill when the user wants to create a Model Context Protocol (MCP) server in Java or in a Spring Boot app. Also use it when the user wants AI agents, such as GitHub Copilot or Claude, to use Java code, an API, or a database. Use it even if the user does not say "MCP". The skill makes a Maven or Gradle project with the MCP Java SDK 2.x, tools, JUnit tests, and client configuration. Do not use it for Quarkus/Quarkiverse MCP servers (use the `quarkus-mcp-server-sse` instruction), for an MCP client or for a server in another language.

This plugin packages the [`java-mcp-server-generator`](skills/java-mcp-server-generator/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/java-mcp-server-generator) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/java-mcp-server-generator/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install java-mcp-server-generator@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Djava-mcp-server-generator),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `java-mcp-server-generator`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
