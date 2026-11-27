# elasticsearch-cluster-health

Diagnose a non-green Elasticsearch cluster and surface the single most likely cause with remediation. Use when an operator reports yellow or red status, unassigned shards, allocation failures, or wants read-only triage before deeper investigation. Teaches replica-vs-primary impact, allocation decider classification, and data-loss awareness.

This plugin packages the [`elasticsearch-cluster-health`](skills/elasticsearch-cluster-health/SKILL.md) skill from
[elastic/agent-skills](https://github.com/elastic/agent-skills/tree/main/skills/elasticsearch/elasticsearch-cluster-health) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/elasticsearch-cluster-health/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install elasticsearch-cluster-health@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Delasticsearch-cluster-health),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `elasticsearch-cluster-health`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[elastic/agent-skills](https://github.com/elastic/agent-skills).
