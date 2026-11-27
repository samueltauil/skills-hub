# test-anti-patterns

Audit a test file or suite; produce a severity-ranked diagnostic report. ALWAYS USE for tests that verify nothing, missing/tautological assertions, swallowed/broad exceptions, flaky/order-dependent tests, duplication, or magic values. Polyglot. DO NOT USE for direct edits: writing-mstest-tests owns supplied MSTest assertions/attributes/lifecycle; code-testing owns new tests. Exclude running tests, migration, assertion metrics (assertion-quality), raw .NET coverage collection (run-tests), non-.NET coverage collection/analysis (native tooling), project-wide .NET coverage/CRAP (coverage-analysis), named-target .NET CRAP (crap-score), behavioral/pseudo-mutation gaps (test-gap-analysis), test-mix/ happy-vs-error classification and trait distributions (test-tagging), or the testsmells.org catalog (test-smell-detection).

This plugin packages the [`test-anti-patterns`](skills/test-anti-patterns/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test/skills/test-anti-patterns) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/test-anti-patterns/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install test-anti-patterns@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dtest-anti-patterns),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `test-anti-patterns`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
