# google-cloud-solution-event-driven-decoupling

Decouples tightly coupled services or monoliths with Google Cloud Pub/Sub so services scale and fail independently, using Go reference implementations adaptable to Java, Python, Node.js, and other stacks. Use when breaking apart synchronous chains, defining transaction boundaries, bulkheads, and Transactional Outbox or post-commit publishing; sizing Pub/Sub topics, subscription filters, dead-letter policies, backoff, 10 MB Cloud Storage claim-check, or database-bounded flow control; building idempotent consumers with ack/nack/quarantine handling, SIGTERM draining, GKE HPA, Cloud Run push, Eventarc, or Cloud Run functions (--retry); or instrumenting OpenTelemetry W3C Trace Context across HTTP, gRPC, and Pub/Sub with Cloud Trace OTLP export and Cloud Logging correlation. Don't use for querying existing traces (use cloud-trace-querying), Kafka or non-Google brokers, or orchestration engines such as Workflows or Managed Service for Apache Airflow.

This plugin packages the [`google-cloud-solution-event-driven-decoupling`](skills/google-cloud-solution-event-driven-decoupling/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/google-cloud-solution-event-driven-decoupling) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/google-cloud-solution-event-driven-decoupling/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install google-cloud-solution-event-driven-decoupling@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgoogle-cloud-solution-event-driven-decoupling),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `google-cloud-solution-event-driven-decoupling`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
