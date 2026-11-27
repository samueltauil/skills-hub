# mimir

Stand up Grafana Mimir for horizontally scalable, multi-tenant, long-term Prometheus + OTLP metrics storage. Covers monolithic / read-write / microservices deployment, S3 / GCS / Azure / filesystem block storage, Prometheus `remote_write` and OTLP ingestion, multi-tenancy with `X-Scope-OrgID`, ingester replication factor, compactor retention, and per-tenant limits. Use when running Mimir locally or on Kubernetes (Helm `mimir-distributed`), scaling Prometheus past a single node, picking ingest / query / backend split, configuring tenants and ingestion rate, debugging `/ready` 503s or `429 Too Many Requests`, or pointing Grafana at a Mimir datasource — even when the user says "I need long-term Prometheus storage", "scale Prometheus", "multi-tenant metrics backend", "Cortex replacement", "remote_write target", or "store 10M active series" without naming Mimir.

This plugin packages the [`mimir`](skills/mimir/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-lgtm/mimir) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/mimir/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install mimir@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmimir),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `mimir`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
