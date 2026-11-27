# test-value-evidence

Assess tests for an identified code or test change, feature, PR or commit. USE FOR: review changed behavior or regression tests, prove pre-fix/missing behavior is detected, revision-bound red-green evidence. Polyglot. DO NOT USE without an identified change: hypothetical mutations or general suite blind spots (test-gap-analysis). Also exclude per-test readiness/A-F grades (grade-tests), coverage (coverage-analysis), new suites (code-testing), or mutation engines.

This plugin packages the [`test-value-evidence`](skills/test-value-evidence/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test/skills/test-value-evidence) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/test-value-evidence/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install test-value-evidence@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dtest-value-evidence),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `test-value-evidence`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
