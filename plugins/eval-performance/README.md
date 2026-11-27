# eval-performance

Diagnose measured MSBuild evaluation cost before targets run. USE FOR: evaluation-only repeats under global-property variants, expensive node_modules/.git/bin/obj globs, import depth >20, /pp >10K lines, file-I/O property functions, five-phase evaluation. DO NOT USE FOR: duplicate executions (find-repeated-work-within-one-build), execution bottlenecks (build-perf-diagnostics), incremental rebuilds (incremental-build), non-MSBuild systems.

This plugin packages the [`eval-performance`](skills/eval-performance/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-msbuild/skills/eval-performance) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/eval-performance/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install eval-performance@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Deval-performance),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `eval-performance`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
