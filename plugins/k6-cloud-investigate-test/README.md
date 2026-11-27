# k6-cloud-investigate-test

Investigate a Grafana Cloud k6 test — describe the script, list run history, identify pass/fail status, pull raw metric time-series and log lines for one or more runs, and (if asked) safely edit the test script. Use when the user asks about a specific k6 cloud test or run, gives a `/a/k6-app/tests/<id>` or `/a/k6-app/runs/<id>` URL, asks "is this test passing", "why are my k6 tests failing", "show me metrics for run X", "show me logs for run X", or wants to add thresholds / fix a failing test. Trigger this skill even when the user doesn't explicitly say "investigate" — pasted `/a/k6-app/...` URLs, "why did run X fail", "what happened with my test", "is my test healthy", "the latest run looks weird", "checks are failing but the run says passed", or any request to diagnose a Grafana Cloud k6 run all qualify.

This plugin packages the [`k6-cloud-investigate-test`](skills/k6-cloud-investigate-test/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-k6/k6-cloud-investigate-test) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/k6-cloud-investigate-test/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install k6-cloud-investigate-test@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dk6-cloud-investigate-test),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `k6-cloud-investigate-test`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
