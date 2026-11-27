# elasticsearch-anomaly-detection-explainer

Explain Elasticsearch ML anomaly detection scores, model behavior, and result interpretation. Use when the user asks why a score is high or low, how the model learns, what the numbers mean, or how to troubleshoot unexpected anomaly scores.

This plugin packages the [`elasticsearch-anomaly-detection-explainer`](skills/elasticsearch-anomaly-detection-explainer/SKILL.md) skill from
[elastic/agent-skills](https://github.com/elastic/agent-skills/tree/main/skills/elasticsearch/elasticsearch-anomaly-detection-explainer) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/elasticsearch-anomaly-detection-explainer/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install elasticsearch-anomaly-detection-explainer@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Delasticsearch-anomaly-detection-explainer),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `elasticsearch-anomaly-detection-explainer`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[elastic/agent-skills](https://github.com/elastic/agent-skills).
