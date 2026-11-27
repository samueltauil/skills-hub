# elasticsearch-reindex

Guide Elasticsearch reindex for performance: local and remote, slicing, throttling, task API. Use when copying or migrating indices, changing mappings, or transforming during reindex.

This plugin packages the [`elasticsearch-reindex`](skills/elasticsearch-reindex/SKILL.md) skill from
[elastic/agent-skills](https://github.com/elastic/agent-skills/tree/main/skills/elasticsearch/elasticsearch-reindex) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/elasticsearch-reindex/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install elasticsearch-reindex@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Delasticsearch-reindex),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `elasticsearch-reindex`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[elastic/agent-skills](https://github.com/elastic/agent-skills).
