# k6-browser-test

Generate a working k6 browser test (k6/browser) from a plain-language description of a user journey — no CSS selectors or technical detail needed. Explores the LIVE target site with a throwaway k6/browser session to discover real, verified selectors (getByRole/getByLabel/getByText, etc.), dismisses cookie/consent banners, then writes a functional or load test using expect() from k6-testing (Web-Vitals thresholds for load). Looks up k6/browser APIs via `k6 x docs`; validates with `k6 run`. Use when the user wants to write, author, or generate a k6 browser/UI or load test with a real browser, or says things like "write a browser test for…", "test this login/checkout/search flow with k6", "click through my site and verify…", or describes navigating a site in prose. For a full multi-test performance suite use k6-perf-test-website; for HTTP/protocol (non-browser) tests use the general k6 skills; for browser or scripted checks in Grafana Cloud Synthetic Monitoring, use synthetic-monitoring-checks.

This plugin packages the [`k6-browser-test`](skills/k6-browser-test/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-k6/k6-browser-test) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/k6-browser-test/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install k6-browser-test@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dk6-browser-test),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `k6-browser-test`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
