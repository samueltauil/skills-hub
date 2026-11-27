# performance-rca

Investigates CPU, memory, and contention problems with Grafana Pyroscope profiles via the gcx CLI. Compares affected and baseline workloads, locates changed application stacks, and tests root-cause hypotheses against symptom and change evidence. Use when a service shows high CPU, growing memory, GC pressure, lock contention, or hot functions, when code regressed after a deploy, or when given a suspect service, flame graph, trace, or profiling anomaly report. For profiling setup use pyroscope; for profilecli-based analysis use profilecli-insights.

This plugin packages the [`performance-rca`](skills/performance-rca/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-lgtm/performance-rca) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/performance-rca/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install performance-rca@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dperformance-rca),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `performance-rca`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
