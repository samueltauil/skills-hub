# alloy

Build a unified telemetry pipeline with Grafana Alloy — one OpenTelemetry-compatible binary that collects metrics, logs, traces, and profiles and ships to Grafana Cloud / Prometheus / Loki / Tempo / Pyroscope. Covers the Alloy config language (blocks, `sys.env`, component refs), `prometheus.scrape` → `remote_write`, `loki.source.file` + `loki.process` → `loki.write`, `otelcol.receiver.otlp` → `otelcol.exporter.otlp`, `pyroscope.scrape`, K8s / Docker / EC2 discovery, relabeling, modules (`import.file/git/http`), clustering, Fleet Management `remotecfg`, the Alloy UI at `:12345`, and `alloy fmt` / `alloy validate`. Use when writing a `config.alloy`, replacing Grafana Agent / OTel Collector, scraping K8s pods, parsing logs, ingesting OTLP, or debugging "Alloy isn't sending anything" — even when the user says "set up the agent", "write me a scrape config", "drop these logs before sending", or "OTel collector config" without naming Alloy.

This plugin packages the [`alloy`](skills/alloy/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-core/alloy) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/alloy/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install alloy@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dalloy),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `alloy`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
