# k6-test-maintenance

Maintain and improve existing k6 test scripts. Covers threshold tightening based on trend data, version migration between k6 releases, auto-fixing tests when the underlying service changes, refactoring for cleanliness, and auditing scripts against current best practices from docs. Use when the user asks to fix a failing k6 test, tighten thresholds, migrate a script to a new k6 version, refactor a test, update a script after a service change, or improve a script with best practices. Trigger on phrases like "fix my k6 test", "tighten my thresholds", "migrate to k6 v2", "update my test script", "refactor this k6 test", "my test is failing after a deploy", "apply best practices to my script", "modernize my k6 test", or "the service changed and my test broke". Also trigger when another skill (k6-trend-analysis or k6-cloud-investigate-test) hands off with a recommendation to edit a script. Maintains existing scripts; to author a new test use the k6 skill, or k6-browser-test for a browser test.

This plugin packages the [`k6-test-maintenance`](skills/k6-test-maintenance/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-k6/k6-test-maintenance) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/k6-test-maintenance/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install k6-test-maintenance@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dk6-test-maintenance),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `k6-test-maintenance`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
