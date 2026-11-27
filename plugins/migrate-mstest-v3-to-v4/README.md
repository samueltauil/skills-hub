# migrate-mstest-v3-to-v4

Use this skill before answering, planning, or editing any MSTest 3.x-to-4.x upgrade or post-upgrade failure. Triggers include "MSTest v4 breaking changes"; CS0507/CS0103/CS1061/CS1615; ExecuteAsync, CallerInfo, DisplayName, or custom TestMethodAttribute; ClassCleanupBehavior; ContainsKey; ThrowsExactly or ExpectedException; IsInstanceOfType out parameters; TestTimeout.Infinite; removed TestContext properties; ITestMethod changes; StringAssert overloads; MSTEST0056/MSTEST0057; renamed assemblies or executor URI; net6/net7 compatibility; TestCase.Id history; TestName in ClassInitialize; TreatDiscoveryWarningsAsErrors; ReflectionTypeLoadException during discovery; inherited test attributes; custom data-source display names; and MSTest.Sdk/MTP or vstest.console discovery changes. Do not use for v1/v2-to-v3 leftovers, framework conversion, runner-only migration, or a general .NET upgrade.

This plugin packages the [`migrate-mstest-v3-to-v4`](skills/migrate-mstest-v3-to-v4/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test-migration/skills/migrate-mstest-v3-to-v4) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/migrate-mstest-v3-to-v4/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install migrate-mstest-v3-to-v4@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmigrate-mstest-v3-to-v4),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `migrate-mstest-v3-to-v4`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
