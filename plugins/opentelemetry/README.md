# opentelemetry

Instrument any app with OpenTelemetry and ship metrics / logs / traces to Grafana Cloud or self-hosted Mimir / Loki / Tempo / Pyroscope. Covers SDK auto-instrumentation for Go, Java (Grafana JVM agent), Python (`opentelemetry-instrument`), Node.js, .NET (`Grafana.OpenTelemetry`), Beyla eBPF for zero-code; Grafana Cloud OTLP gateway + Basic-auth (instanceID + API key, base64); env-var config (`OTEL_EXPORTER_OTLP_*`, `OTEL_RESOURCE_ATTRIBUTES`); Alloy / OTel-Collector pipelines; Kubernetes Operator inject-annotations; and head + tail sampling. Use when instrumenting a service, pointing OTLP at Grafana Cloud, switching from Jaeger / Datadog / New Relic, choosing head- vs tail-sampling, or debugging "spans aren't showing in Explore" — even when the user says "auto-instrument my Java app", "send traces to Grafana", "what env vars do I set", "OTLP endpoint", or "Operator inject" without naming OpenTelemetry.

This plugin packages the [`opentelemetry`](skills/opentelemetry/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-core/opentelemetry) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/opentelemetry/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install opentelemetry@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dopentelemetry),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `opentelemetry`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
