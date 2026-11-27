# check-bin-obj-clash

Find OutputPath/IntermediateOutputPath collisions between distinct projects or required property/TFM variants. USE FOR: missing/overwritten bin/obj or project.assets.json, parallel 'Cannot create a file when that file already exists' or 'file is being used by another process', shared paths, missing AppendTargetFrameworkToOutputPath, PublishReadyToRun, SetTargetFramework on single-target references. DO NOT USE FOR: duplicates or invariant-generation races (find-repeated-work-within-one-build), OS locking, single-instance builds, non-MSBuild systems.

This plugin packages the [`check-bin-obj-clash`](skills/check-bin-obj-clash/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-msbuild/skills/check-bin-obj-clash) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/check-bin-obj-clash/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install check-bin-obj-clash@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcheck-bin-obj-clash),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `check-bin-obj-clash`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
