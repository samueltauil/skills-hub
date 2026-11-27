# find-untested-sources

MANDATORY for static source-to-test pairing: find or list source files/modules without corresponding tests, or suggest test locations from repository structure. Invoke even for a tiny package; do not substitute manual globbing. Uses Roslyn for C#/.NET and tree-sitter for Python, TS/JS, Go, Java, Rust, Ruby, Kotlin, Swift, PowerShell, and C++. DO NOT USE FOR: real line/branch/Cobertura data, coverage-backed test priorities, CRAP risk, or grading existing tests.

This plugin packages the [`find-untested-sources`](skills/find-untested-sources/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test/skills/find-untested-sources) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/find-untested-sources/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install find-untested-sources@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dfind-untested-sources),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `find-untested-sources`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
