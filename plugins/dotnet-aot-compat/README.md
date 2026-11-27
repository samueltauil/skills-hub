# dotnet-aot-compat

Make .NET projects compatible with Native AOT and trimming by systematically resolving IL trim/AOT analyzer warnings. USE FOR: making projects AOT-compatible, fixing trimming warnings, resolving IL warnings (IL2026, IL2070, IL2067, IL2072, IL3050), adding DynamicallyAccessedMembers annotations, enabling IsAotCompatible. DO NOT USE FOR: publishing native AOT binaries, optimizing binary size, replacing reflection-heavy libraries with alternatives. INVOKES: no tools — pure knowledge skill.

This plugin packages the [`dotnet-aot-compat`](skills/dotnet-aot-compat/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-upgrade/skills/dotnet-aot-compat) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/dotnet-aot-compat/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install dotnet-aot-compat@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddotnet-aot-compat),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `dotnet-aot-compat`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
