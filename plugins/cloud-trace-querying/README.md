# cloud-trace-querying

Query Cloud Trace spans, filter by latency thresholds or error status, correlate distributed traces with Cloud Logging, and diagnose latency bottlenecks across Google Cloud services. Use when investigating slow requests, analyzing trace hierarchies, or resolving latency regressions. Do NOT use for querying non-GCP telemetry or database query optimization outside Cloud Trace.

This plugin packages the [`cloud-trace-querying`](skills/cloud-trace-querying/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/cloud-trace-querying) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/cloud-trace-querying/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install cloud-trace-querying@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcloud-trace-querying),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `cloud-trace-querying`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
