# including-generated-files

Own MSBuild generated-artifact integration. USE FOR: a target that creates or should create source, Content, None, or another physical file but the artifact is missing from compilation or output; target timing; evaluation-time glob misses; $(IntermediateOutputPath) placement; and FileWrites clean tracking. The prompt may describe the generated artifact without naming the producing task. DO NOT USE when the primary defect is general Include/Remove/Update semantics, item metadata or batching, duplicate/overlapping declarations, or a generated-item identity relationship; use item-management. Exclude Roslyn source-generator internals and non-MSBuild systems.

This plugin packages the [`including-generated-files`](skills/including-generated-files/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-msbuild/skills/including-generated-files) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/including-generated-files/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install including-generated-files@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dincluding-generated-files),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `including-generated-files`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
