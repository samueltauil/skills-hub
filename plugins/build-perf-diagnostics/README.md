# build-perf-diagnostics

Diagnose MSBuild bottlenecks from binlog timelines and Target/Task Performance Summaries after baseline measurements. USE FOR: unknown build slowness, RAR >5s, analyzers >30% of Csc, a target >50% of build, node utilization below 80%, excessive Copy, restore overhead. DO NOT USE FOR: within-build duplicates (find-repeated-work-within-one-build), known repeated restores (eliminate-redundant-restores), initial baselines (build-perf-baseline), incremental rebuilds (incremental-build), parallelism tuning (build-parallelism), non-MSBuild builds.

This plugin packages the [`build-perf-diagnostics`](skills/build-perf-diagnostics/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-msbuild/skills/build-perf-diagnostics) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/build-perf-diagnostics/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install build-perf-diagnostics@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dbuild-perf-diagnostics),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `build-perf-diagnostics`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
