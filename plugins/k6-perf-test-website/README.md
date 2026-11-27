# k6-perf-test-website

Use when the user wants to performance-test, load-test, or stress-test a public website end-to-end with k6. Produces a hybrid (protocol + browser) test suite, SLO-backed thresholds, a load-generator monitor sidecar, and a Grafana-side investigation playbook for backends the user owns. Triggers on "perf test my site", "performance test my site", "load test this URL", "stress test my web app", "I want to load test [URL]", "set up k6 against my website", "write a k6 suite for [site]", "see if my site handles N concurrent users", or "how does my site perform under traffic". Use this skill whenever the user mentions k6, load testing, stress testing, performance testing, or wants to validate a website under traffic — even if they don't explicitly use the word "test" or ask for the specific outputs this skill produces. This skill is for a full multi-test suite across several workflows; for a single browser test — functional OR a browser load test measuring Web Vitals for one journey — use k6-browser-test.

This plugin packages the [`k6-perf-test-website`](skills/k6-perf-test-website/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-k6/k6-perf-test-website) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/k6-perf-test-website/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install k6-perf-test-website@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dk6-perf-test-website),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `k6-perf-test-website`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
