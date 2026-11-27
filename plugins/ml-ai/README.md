# ml-ai

Turn on AI + ML features in Grafana Cloud — Grafana Assistant (NL → PromQL/LogQL/TraceQL, dashboard build, incident investigation, MCP integration), Dynamic Alerting (Prophet forecasting + DBSCAN outlier detection), Sift (8-analysis automated root-cause), Knowledge Graph + RCA Workbench, and the LLM Plugin (OpenAI / Anthropic / Azure / Ollama / vLLM / LiteLLM). Use when you want anomaly alerts without static thresholds, natural-language querying, automated incident investigation, dashboards generated from a sentence, or a managed LLM proxy for plugins — even when the user says "alert when something looks weird", "explain this PromQL", "find the root cause", "make this a dashboard", or "wire Claude into Grafana" without naming any of these products.

This plugin packages the [`ml-ai`](skills/ml-ai/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-cloud/ml-ai) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/ml-ai/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install ml-ai@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dml-ai),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `ml-ai`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
