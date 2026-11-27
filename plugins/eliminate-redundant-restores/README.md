# eliminate-redundant-restores

Remove repeated NuGet restores from multi-step .NET builds safely. USE FOR: build/test/publish steps that each restore, Directory.Build.rsp with -restore, safe restore suppression, NETSDK1004/NETSDK1047 after --no-restore. DO NOT USE FOR: slow first restore, only one restore, version or lock errors, unranked build slowness (use build-perf-baseline).

This plugin packages the [`eliminate-redundant-restores`](skills/eliminate-redundant-restores/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-msbuild/skills/eliminate-redundant-restores) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/eliminate-redundant-restores/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install eliminate-redundant-restores@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Deliminate-redundant-restores),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `eliminate-redundant-restores`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
