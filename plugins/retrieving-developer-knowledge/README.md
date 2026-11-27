# retrieving-developer-knowledge

Searches, retrieves, and synthesizes official Google developer documentation across Google Cloud, AI/Gemini, Android, Chrome, Web, Flutter, Go, Firebase, and other Google developer platforms. Integrates with the Developer Knowledge MCP server (search_documents, get_documents, answer_query) or the Developer Knowledge REST API fallback. Use when searching for gcloud CLI commands, API syntax, IAM permissions, official documentation, architectural comparisons, or product choice overviews. Don't use for local filesystem lookups or non-Google documentation.

This plugin packages the [`retrieving-developer-knowledge`](skills/retrieving-developer-knowledge/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/developers/retrieving-developer-knowledge) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/retrieving-developer-knowledge/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install retrieving-developer-knowledge@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dretrieving-developer-knowledge),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `retrieving-developer-knowledge`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
