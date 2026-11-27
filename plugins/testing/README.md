# testing

Probe, load-test, and instrument frontends from Grafana Cloud. Covers Synthetic Monitoring (HTTP / DNS / TCP / Ping / Traceroute / Multihttp / k6-browser scripted checks from 20+ global probes, alert on `probe_success` + TLS-cert expiry), Grafana Cloud k6 (distributed load tests across AWS load-zones, scenarios, `http_req_duration` thresholds, CI integration via `grafana/k6-action`), and Frontend Observability with Faro Web SDK (RUM, Core Web Vitals, custom events, `pushError`, distributed-trace correlation). Use when checking website / API uptime from multiple regions, gating a release on a load test, watching for TLS-cert renewal, instrumenting a React/Vue app, tracking Core Web Vitals, or correlating frontend errors to backend traces — even when the user says "is my login flow up?", "monitor my API", "ping our endpoint every minute", "release-gate load test", "browser performance monitoring", "session replay", or "RUM" without naming Synthetic Monitoring / k6 / Faro.

This plugin packages the [`testing`](skills/testing/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-cloud/testing) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/testing/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install testing@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dtesting),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `testing`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
