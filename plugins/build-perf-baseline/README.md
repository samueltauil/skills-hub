# build-perf-baseline

Establish MSBuild/.NET baselines before optimizing. USE FOR: unranked slow builds; cold/warm/incremental/no-op measurements; before/after comparisons; CI caching; static graph, artifacts output, dependency graph trimming. DO NOT USE FOR: measured bottlenecks (build-perf-diagnostics), known repeated restores (eliminate-redundant-restores), within-build duplicate calls (find-repeated-work-within-one-build), non-MSBuild builds.

This plugin packages the [`build-perf-baseline`](skills/build-perf-baseline/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-msbuild/skills/build-perf-baseline) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/build-perf-baseline/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install build-perf-baseline@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dbuild-perf-baseline),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `build-perf-baseline`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
