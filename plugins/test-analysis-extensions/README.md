# test-analysis-extensions

Provides file paths to language-specific reference files for the test ANALYSIS skills (assertion-quality, test-anti-patterns, test-gap-analysis, test-smell-detection, test-tagging). Read this catalog to discover available extension files (e.g., dotnet.md for .NET/MSTest/xUnit/NUnit/TUnit, python.md for pytest/unittest, typescript.md for Jest/Vitest/Mocha, java.md for JUnit/TestNG, etc.). Do not invoke this reference-only skill — its bundled files are read by the quality agent and analysis skills needing framework-specific lookup tables (test markers, assertion APIs, skip annotations, sleep patterns, mystery guest indicators, integration markers, setup/teardown, tag-support capability).

This plugin packages the [`test-analysis-extensions`](skills/test-analysis-extensions/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test/skills/test-analysis-extensions) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/test-analysis-extensions/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install test-analysis-extensions@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dtest-analysis-extensions),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `test-analysis-extensions`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
