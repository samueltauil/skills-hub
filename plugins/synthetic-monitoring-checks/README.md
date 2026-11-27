# synthetic-monitoring-checks

Author Grafana Cloud Synthetic Monitoring checks, with deep coverage of k6 scripted and browser checks: SM's single-VU/single-iteration execution model, assertions that actually fail probe_success (expect() and fail() vs bare check()), secrets, deterministic scripts, robust browser locators, local validation with k6 run, deployment via UI/API/Terraform, verifying probe_success, and rollback. Also helps choose the simplest sufficient check type (HTTP/ping/DNS/TCP, MultiHTTP, scripted, browser). Use when writing a synthetic check, monitoring a login/checkout/signup flow in production, converting a k6 script or an OpenAPI spec into a check, authoring a browser check, validating a user journey, or asking "is my site up from multiple regions". NOT for load, stress, or performance testing — SM runs one iteration per execution; for load tests use the grafana-k6 plugin or Grafana Cloud k6. For the broad Grafana Cloud Testing overview (SM + k6 Cloud + Faro), use the testing skill.

This plugin packages the [`synthetic-monitoring-checks`](skills/synthetic-monitoring-checks/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-cloud/synthetic-monitoring-checks) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/synthetic-monitoring-checks/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install synthetic-monitoring-checks@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsynthetic-monitoring-checks),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `synthetic-monitoring-checks`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
