# tempo

Stand up Grafana Tempo as a cost-efficient distributed-tracing backend that only needs object storage, and write TraceQL queries against it. Covers OTLP + Jaeger + Zipkin ingestion, the distributor → live-store → block-builder → object-storage write path, metrics-generator for RED spanmetrics + service graphs, Helm `tempo-distributed` deployment, multi-tenant `X-Scope-OrgID`, TraceQL span / resource / event scopes, structural operators (`>>`, `<<`), `rate()` + `quantile_over_time` metrics, and the traces-to-logs / metrics / profiles datasource links. Use when deploying Tempo, writing a TraceQL query for slow / errored requests, debugging "no traces showing in Explore", sizing queriers / compactors, configuring S3 / GCS / Azure block storage, or wiring trace ↔ log ↔ profile correlation — even when the user says "tracing backend", "find slow requests", "show me the service graph", "store traces in S3", "Jaeger compatible store", or "what called this span" without naming Tempo.

This plugin packages the [`tempo`](skills/tempo/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-lgtm/tempo) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/tempo/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install tempo@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dtempo),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `tempo`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
