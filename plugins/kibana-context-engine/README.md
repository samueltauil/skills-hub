# kibana-context-engine

Query Elastic Context Engine AI Indices, and the Knowledge Indicators (KIs) they store. Use when asked to search, explore, count, or answer questions from an AI Index / KI / Context Engine knowledge index, and when writing the ES|QL that queries one.

This plugin packages the [`kibana-context-engine`](skills/kibana-context-engine/SKILL.md) skill from
[elastic/agent-skills](https://github.com/elastic/agent-skills/tree/main/skills/kibana/kibana-context-engine) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/kibana-context-engine/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install kibana-context-engine@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dkibana-context-engine),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `kibana-context-engine`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[elastic/agent-skills](https://github.com/elastic/agent-skills).
