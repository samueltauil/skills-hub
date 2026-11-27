# extension-points

Own MSBuild import and hook discovery. USE FOR: CustomBefore/CustomAfter hooks, ordered wildcard and NuGet auto-imports, control properties, build/buildTransitive packed layout, package ID and file-name matching, per-TFM forwarders, and tracing why assets or hooks are missing, broken, or replaced. An import guard remains in scope when it is one defect in a broader hook/import flow. DO NOT USE for a focused safety verdict on whether one specific Import needs Exists or is an intentionally unguarded package contract; use msbuild-antipatterns. NEVER INVOKE when imports and hook placement already work and the request is only target Inputs/Outputs, incremental skipping, or FileWrites clean tracking; use incremental-build or target-authoring. Exclude props-versus-targets placement and non-MSBuild systems.

This plugin packages the [`extension-points`](skills/extension-points/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-msbuild/skills/extension-points) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/extension-points/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install extension-points@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dextension-points),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `extension-points`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
