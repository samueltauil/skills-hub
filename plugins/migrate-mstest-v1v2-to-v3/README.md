# migrate-mstest-v1v2-to-v3

Use this skill before answering or editing whenever an MSTest v1/v2 project is being upgraded or repaired for v3. Triggers include QualityTools assembly references; MSTest.TestFramework/TestAdapter 1.x-2.x; "upgrade to MSTest v3"; comparing v1 and v2 migration paths; choosing MSTest or MSTest.Sdk; CS0411/CS1503 after a v3 package bump; DataRow type mismatch, MSTEST0014, or "Test data doesn't match method parameters"; .testsettings/LegacySettings to .runsettings; timeout changes; and net5.0 or other dropped v3 TFMs. Still use it when packages say 3.x but migration source errors or legacy settings remain. Preserve VSTest/MTP. Do not use for a clean v3 project, v3-to-v4, framework conversion, or runner-only migration.

This plugin packages the [`migrate-mstest-v1v2-to-v3`](skills/migrate-mstest-v1v2-to-v3/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test-migration/skills/migrate-mstest-v1v2-to-v3) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/migrate-mstest-v1v2-to-v3/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install migrate-mstest-v1v2-to-v3@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmigrate-mstest-v1v2-to-v3),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `migrate-mstest-v1v2-to-v3`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
