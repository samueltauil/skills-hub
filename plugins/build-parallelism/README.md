# build-parallelism

Analyze MSBuild scheduling across at least two distinct projects in a solution/filter/Build.proj. USE FOR: measured idle workers, -m not scaling, serial ProjectReference critical paths, graph builds, MSBuild Projects-list scheduling. DO NOT USE FOR: duplicate executions or invariant-generation races (find-repeated-work-within-one-build), non-MSBuild systems.

This plugin packages the [`build-parallelism`](skills/build-parallelism/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-msbuild/skills/build-parallelism) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/build-parallelism/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install build-parallelism@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dbuild-parallelism),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `build-parallelism`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
