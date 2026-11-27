# k6-manage

Interact with Grafana Cloud k6 (GCk6) — manage load tests, test runs, scripts, projects, schedules, env vars, fetch metrics or logs, and run scripts locally — using the `gcx` CLI (or direct curl when gcx is unavailable). Use this skill whenever the user mentions a k6 cloud test or run, asks to list/edit/create/start/abort k6 load tests, wants to fetch logs or metrics for a test run, manage k6 project limits or schedules, run a k6 script locally or via `k6 cloud run`, or needs to call any `/cloud/v6/`, `/cloud/v5/`, or k6-app Loki endpoint against a Grafana Cloud stack. Trigger even when the user doesn't explicitly say "gcx" or "API" — phrases like "why did my k6 test fail", "show me logs for run X", "bump VUh limit on project Y", or "update my k6 script" all qualify.

This plugin packages the [`k6-manage`](skills/k6-manage/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-k6/k6-manage) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/k6-manage/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install k6-manage@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dk6-manage),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `k6-manage`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
