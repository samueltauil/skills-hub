# microbenchmarking

Activate this skill when BenchmarkDotNet (BDN) is involved in the task — creating, running, configuring, or reviewing BDN benchmarks. Also activate when microbenchmarking .NET code would be useful and BenchmarkDotNet is the likely tool. Consider activating when answering a .NET performance question requires measurement and BenchmarkDotNet may be needed. Covers microbenchmark design, BDN configuration and project setup, how to run BDN microbenchmarks efficiently and effectively, and using BDN for side-by-side performance comparisons. Do NOT use for profiling/tracing .NET code (dotnet-trace, PerfView), production telemetry, or load/stress testing (Crank, k6).

This plugin packages the [`microbenchmarking`](skills/microbenchmarking/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-diag/skills/microbenchmarking) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/microbenchmarking/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install microbenchmarking@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmicrobenchmarking),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `microbenchmarking`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
