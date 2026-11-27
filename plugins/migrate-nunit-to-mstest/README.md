# migrate-nunit-to-mstest

Convert .NET tests from NUnit 3/4 to MSTest v4 while preserving VSTest or MTP. Use for replacing NUnit/NUnit3TestAdapter packages, Test/TestCase/ TestCaseSource/Values attributes, constraint assertions, SetUp/TearDown, OneTimeSetUp, SetUpFixture, FixtureLifeCycle, TestContext, categories, retries, timeouts, and NUnit parallelization. Also use when a "convert NUnit to MSTest" request may already be migrated: inspect and report the no-op. Do not use for NUnit version upgrades, xUnit/TUnit conversion, MSTest upgrades, or runner-only VSTest-to-MTP migration.

This plugin packages the [`migrate-nunit-to-mstest`](skills/migrate-nunit-to-mstest/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test-migration/skills/migrate-nunit-to-mstest) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/migrate-nunit-to-mstest/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install migrate-nunit-to-mstest@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmigrate-nunit-to-mstest),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `migrate-nunit-to-mstest`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
