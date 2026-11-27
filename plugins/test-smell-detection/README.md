# test-smell-detection

Audits existing tests in any language using formal, research-backed test smell names and the testsmells.org 19-smell academic taxonomy. Use when the caller asks for an academic or citable test-smell review, named smell categories, or a formal severity-ranked smell assessment. Covers Assertion Roulette, Conditional Test Logic, Mystery Guest, Eager Test, Sleepy Test, Unknown Test, Sensitive Equality, and the rest of the catalog across .NET, Python, JavaScript/TypeScript, Java, Go, Ruby, Rust, Swift, Kotlin, PowerShell, and C++. DO NOT USE FOR a quick pragmatic test review (use test-anti-patterns), writing or running tests, framework migration, coverage, or assertion-diversity metrics.

This plugin packages the [`test-smell-detection`](skills/test-smell-detection/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test/skills/test-smell-detection) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/test-smell-detection/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install test-smell-detection@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dtest-smell-detection),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `test-smell-detection`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
