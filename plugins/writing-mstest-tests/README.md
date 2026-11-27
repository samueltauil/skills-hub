# writing-mstest-tests

ALWAYS USE when asked to fix, rewrite, update, improve, modernize, show corrected code for, or explain existing MSTest tests or MSTest-specific configuration. Use for "review" when corrected code or edits are wanted, even for one pasted assertion or passing tests with bad failure output. Covers expected/actual labels; generic Boolean, collection, string, numeric, null, identity, exception, hard-cast, and object[] checks; TestContext/lifecycle; timeout/cancellation; OS/CI conditions, retry, cleanup, parallelization, MSTest.Sdk project setup, and MSTESTxxxx. Honor the installed MSTest version. DO NOT USE to design new test cases (code-testing), perform report-only audits, create project files rather than explain MSTest setup, run tests, migrate frameworks, or handle non-MSTest/non-.NET code.

This plugin packages the [`writing-mstest-tests`](skills/writing-mstest-tests/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test/skills/writing-mstest-tests) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/writing-mstest-tests/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install writing-mstest-tests@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dwriting-mstest-tests),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `writing-mstest-tests`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
