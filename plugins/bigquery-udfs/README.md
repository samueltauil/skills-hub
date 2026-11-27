# bigquery-udfs

Creates, deploys, and troubleshoots BigQuery User-Defined Functions (UDFs) and Remote Functions across SQL, JavaScript, Python, and Cloud Run endpoints. Use when writing custom scalar or aggregate functions in BigQuery, installing PyPI packages or Cloud Storage libraries in a Python or JavaScript UDF, or calling Google Cloud and external APIs from a Python UDF (WITH CONNECTION) or Remote Function. Don't use for standard BigQuery table/dataset CRUD (use bigquery-basics), DataFrames client workflows (use bigquery-bigframes), or BigQuery ML models (use bigquery-ai-ml).

This plugin packages the [`bigquery-udfs`](skills/bigquery-udfs/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/bigquery-udfs) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/bigquery-udfs/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install bigquery-udfs@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dbigquery-udfs),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `bigquery-udfs`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
