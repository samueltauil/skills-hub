# beyla

Auto-instrument an application's HTTP / gRPC / DB traffic with Grafana Beyla eBPF — no code changes, no SDK, no restart. Covers requirements (Linux 5.8+ with BTF, CAP_SYS_ADMIN, host PID), language matrix (Go / Java / Python / Ruby / Node / .NET / Rust / C++ / PHP), Docker + Helm + DaemonSet install, port- / process- / Kubernetes-metadata discovery, OTLP traces + Prometheus metrics export, routes decorator (cardinality control), trace sampling, and Grafana Cloud via Alloy. Use when adding observability to a service you can't recompile, instrumenting a closed-source binary, getting RED metrics + spans onto Tempo/Mimir without touching the app, or rolling Beyla as a cluster-wide DaemonSet — even when the user says "zero-code APM", "instrument legacy app", "trace this binary", "eBPF observability", or "no SDK" without naming Beyla.

This plugin packages the [`beyla`](skills/beyla/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-core/beyla) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/beyla/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install beyla@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dbeyla),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `beyla`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
