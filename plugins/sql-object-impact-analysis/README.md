# sql-object-impact-analysis

Before modifying a table, column, stored procedure, view, or trigger in a legacy codebase, trace every place that references it — across other SQL objects (procs, views, triggers) AND application code (C#, Angular/TypeScript, JS, or any language in the repo) — and produce a structured blast-radius report so you know what breaks before you change it. Use when the user asks 'what uses this column/table/procedure', 'is it safe to change X', 'what depends on this', 'impact of renaming/dropping X', or before any schema/proc modification in an unfamiliar or legacy codebase. Not for privacy/PII exposure analysis (see data-breach-blast-radius) or query performance tuning (see sql-optimization).

This plugin packages the [`sql-object-impact-analysis`](skills/sql-object-impact-analysis/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/sql-object-impact-analysis) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/sql-object-impact-analysis/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install sql-object-impact-analysis@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsql-object-impact-analysis),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `sql-object-impact-analysis`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
