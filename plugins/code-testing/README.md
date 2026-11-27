# code-testing

ALWAYS USE for test work that requires changes: write, add, generate, repair, or strengthen tests for existing code in xUnit, MSTest, NUnit, pytest, Vitest/Jest, Go, or another framework. Includes regression cases, failing or flaky tests, coverage-driven additions, and audit-then-fix requests. Focused work stays direct; broad or multi-stage work invokes test-engineer. DO NOT USE for only running tests, analysis-only audits, framework/platform migrations, a test blocked on a missing production seam (testability-obstacle), or MSTest API/configuration corrections that do not design new cases (writing-mstest-tests). Within an active test-engineer pipeline, reuse supplied guidance and do not re-enter this skill.

This plugin packages the [`code-testing`](skills/code-testing/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test/skills/code-testing) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/code-testing/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install code-testing@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcode-testing),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `code-testing`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
