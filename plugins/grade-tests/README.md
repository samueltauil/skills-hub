# grade-tests

Grade curated individual tests for readiness, A-F quality and improvements. ALWAYS USE FOR: grade tests, review only a named test, per-test readiness or quality bands for supplied methods, bodies, file spans or bounded PR diffs, including existing tests. Return Pass/Failed/Uncertain/Not applicable; unresolved/empty scopes omit grades. Compose read-only per-test evidence. Polyglot. DO NOT USE FOR: suite audits (test-engineer/test-anti-patterns), concrete fix/feature detection proof (test-value-evidence), writing/fixing tests, or coverage.

This plugin packages the [`grade-tests`](skills/grade-tests/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test/skills/grade-tests) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/grade-tests/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install grade-tests@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgrade-tests),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `grade-tests`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
