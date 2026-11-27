# migrate-xunit-to-mstest

Convert .NET tests from xUnit.net v2/v3 to MSTest v4 while preserving VSTest or MTP. Use for replacing xunit packages, Fact/Theory/InlineData/MemberData, assertions, IClassFixture/ICollectionFixture, ITestOutputHelper, TestContext cancellation, traits/Owner, skips, timeouts, and xUnit parallelization. Also use when a "convert xUnit to MSTest" request may already be migrated: inspect and report the no-op. Do not use for xUnit v2-to-v3, MSTest upgrades, NUnit/TUnit conversion, or runner-only VSTest-to-MTP migration.

This plugin packages the [`migrate-xunit-to-mstest`](skills/migrate-xunit-to-mstest/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test-migration/skills/migrate-xunit-to-mstest) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/migrate-xunit-to-mstest/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install migrate-xunit-to-mstest@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmigrate-xunit-to-mstest),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `migrate-xunit-to-mstest`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
