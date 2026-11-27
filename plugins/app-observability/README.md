# app-observability

Get RED metrics + service maps + frontend RUM + AI/LLM monitoring out of Grafana Cloud — Application Observability (`traces_spanmetrics_*` from OTel traces, p50/p95/p99 latency, exemplar-to-trace, traces-to-logs / profiles), Frontend Observability with the Faro Web SDK (Core Web Vitals, session replay, `pushError`, React + router integration, `TracingInstrumentation` for browser → backend trace correlation), and AI Observability via OpenLIT (token / cost / latency, GPU, hallucination + toxicity evals). Use when standing up APM for a service, wiring an Alloy OTLP receiver + forwarding to Cloud, instrumenting a React frontend for RUM, debugging why service-map edges are missing, monitoring LLM cost drift, or correlating a frontend error to its backend trace — even when the user says "set up APM", "show service map", "monitor browser perf", "session replay", "RUM SDK", or "watch our OpenAI bill" without naming App / Frontend / AI Observability.

This plugin packages the [`app-observability`](skills/app-observability/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-cloud/app-observability) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/app-observability/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install app-observability@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dapp-observability),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `app-observability`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
