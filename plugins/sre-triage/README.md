# sre-triage

Triage a degraded or suspect service end to end: read SLO status and burn rate, check active alerting rules and ML anomalies, measure throughput, latency, and error rate, assess dependency health and infrastructure saturation, and funnel logs down to the failures that explain it. Use when someone asks whether a service is healthy, why it is slow or erroring, what is in its logs, or which attribute distinguishes the requests that are failing. Also use when someone asks for the query behind any of those signals — throughput, latency percentiles, error rate, dependency health, or log volume — over APM/OTel traces, metrics, or logs.

This plugin packages the [`observability-sre-triage`](skills/observability-sre-triage/SKILL.md) skill from
[elastic/agent-skills](https://github.com/elastic/agent-skills/tree/main/skills/observability/sre-triage) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/sre-triage/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install sre-triage@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsre-triage),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `sre-triage`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[elastic/agent-skills](https://github.com/elastic/agent-skills).
