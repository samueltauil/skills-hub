# bigquery-ai-ml

Leverages BigQuery's built-in machine learning and GenAI capabilities for advanced data analytics. Use when you need to write SQL queries that perform time-series forecasting, predict values, detect outliers or anomalies, find key drivers, perform semantic search or vector search, classify text, calculate similarity, summarize content, translate language, evaluate models, filter by semantic conditions, measure the causal effect of an intervention, compute correlations between columns, generate descriptive statistics and table distribution profiles, detect change points or structural breaks, extract trend or seasonality components, or leverage generative AI capabilities in BigQuery. Do not use for general BigQuery dataset, table, or job management requests.

This plugin packages the [`bigquery-ai-ml`](skills/bigquery-ai-ml/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/bigquery-ai-ml) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/bigquery-ai-ml/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install bigquery-ai-ml@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dbigquery-ai-ml),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `bigquery-ai-ml`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
