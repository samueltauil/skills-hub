# copy-to-output-directory

Choosing an MSBuild CopyToOutputDirectory / CopyToPublishDirectory mode: Never, PreserveNewest, Always, and IfDifferent (MSBuild 17.13+), plus $(SkipUnchangedFilesOnCopyAlways). USE FOR: removing the per-build Always copy perf hit; resetting output files mutated between builds. DO NOT USE FOR: general incremental-build diagnosis (use incremental-build); non-MSBuild build systems.

This plugin packages the [`copy-to-output-directory`](skills/copy-to-output-directory/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-msbuild/skills/copy-to-output-directory) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/copy-to-output-directory/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install copy-to-output-directory@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcopy-to-output-directory),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `copy-to-output-directory`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
