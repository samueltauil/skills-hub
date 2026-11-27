# mini-context-graph

A persistent, compounding knowledge base combining Karpathy's LLM Wiki pattern with a structured knowledge graph. Ingest documents once — the LLM writes wiki pages, extracts entities/relations into the graph, and stores raw content for evidence retrieval. Knowledge accumulates and cross-references; it is never re-derived from scratch.

This plugin packages the [`mini-context-graph`](skills/mini-context-graph/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/mini-context-graph) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/mini-context-graph/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install mini-context-graph@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmini-context-graph),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `mini-context-graph`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
