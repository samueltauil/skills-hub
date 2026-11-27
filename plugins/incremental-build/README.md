# incremental-build

Fix MSBuild incremental/no-op builds: 'nothing changed but it rebuilds anyway'. USE FOR: targets re-executing on subsequent builds, missing Inputs/Outputs or FileWrites, volatile output paths, untracked writes, glob changes, Visual Studio Fast Up-to-Date Check (FUTDC); 'Building target completely' vs 'Skipping target' in binlog. DO NOT USE FOR: within-build duplicates (find-repeated-work-within-one-build), first-build slowness (build-perf-baseline), parallelism (build-parallelism), slow evaluation (eval-performance), non-MSBuild systems.

This plugin packages the [`incremental-build`](skills/incremental-build/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-msbuild/skills/incremental-build) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/incremental-build/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install incremental-build@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dincremental-build),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `incremental-build`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
