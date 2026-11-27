# roslyn-analyzers

Build, review, debug, package, and test Roslyn diagnostic analyzers, code fix providers, and incremental source generators. Use for DiagnosticAnalyzer, CodeFixProvider, IIncrementalGenerator, IOperation analysis, Microsoft.CodeAnalysis dependency pinning, Roslyn test harnesses, C#/VB tests, and analyzer NuGet packaging.

This plugin packages the [`roslyn-analyzers`](skills/roslyn-analyzers/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/roslyn-analyzers) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/roslyn-analyzers/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install roslyn-analyzers@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Droslyn-analyzers),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `roslyn-analyzers`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
