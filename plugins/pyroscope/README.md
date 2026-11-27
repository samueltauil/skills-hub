# pyroscope

Continuously profile applications with Grafana Pyroscope and read the result as flame graphs. Covers three instrumentation paths — language SDK push (Go / Java / Python / Ruby / Node / .NET / Rust), Alloy eBPF auto-instrumentation (no code change, requires kernel 5.8+ with BTF), and SDK → Alloy receiver — plus ProfileQL queries, profile types (CPU / memory / allocations / goroutines / mutex), Grafana Cloud Profiles endpoint, and Span Profiles trace-to-profile linking. Use when adding profiling to a service, deploying Alloy as a cluster-wide eBPF profiler, hunting CPU / memory hotspots from a flame graph, comparing two profiles to find a regression, or correlating a slow Tempo trace to its profile — even when the user says "find what's burning CPU", "flame graph this app", "continuous profiling", "heap hotspots", or "why is allocation so high" without naming Pyroscope.

This plugin packages the [`pyroscope`](skills/pyroscope/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-lgtm/pyroscope) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/pyroscope/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install pyroscope@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpyroscope),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `pyroscope`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
