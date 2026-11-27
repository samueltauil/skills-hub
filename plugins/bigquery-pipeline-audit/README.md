# bigquery-pipeline-audit

Audits Python + BigQuery pipelines for cost safety, idempotency, and production readiness. Returns a structured report with exact patch locations.

This plugin packages the [`bigquery-pipeline-audit`](skills/bigquery-pipeline-audit/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/bigquery-pipeline-audit) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/bigquery-pipeline-audit/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install bigquery-pipeline-audit@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dbigquery-pipeline-audit),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `bigquery-pipeline-audit`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
