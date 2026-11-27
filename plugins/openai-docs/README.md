# openai-docs

Use when the user asks how to build with OpenAI products or APIs, asks about Codex itself or choosing Codex surfaces, needs up-to-date official documentation with citations, help choosing the latest model for a use case, or model upgrade and prompt-upgrade guidance; use OpenAI docs MCP tools for non-Codex docs questions, use the Codex manual helper first for broad Codex self-knowledge, and restrict fallback browsing to official OpenAI domains.

This plugin packages the [`openai-docs`](skills/openai-docs/SKILL.md) skill from
[openai/skills](https://github.com/openai/skills/tree/main/skills/.curated/openai-docs) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/openai-docs/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install openai-docs@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dopenai-docs),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `openai-docs`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[openai/skills](https://github.com/openai/skills).
