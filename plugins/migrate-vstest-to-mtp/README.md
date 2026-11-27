# migrate-vstest-to-mtp

Use this skill before answering, planning, or editing whenever .NET tests or CI are switching from VSTest to Microsoft.Testing.Platform (MTP), or an MTP migration behaves differently. Triggers include "switch from VSTest"; MSTest/NUnit/xUnit MTP enablement; OutputType=Exe only for test projects in Directory.Build.props; EnableMSTestRunner, EnableNUnitRunner, UseMicrosoftTestingPlatformRunner, or YTest.MTP.XUnit2; .NET 10 global.json test.runner and TestingPlatformDotnetTestSupport; translating VSTest filters, logger, coverage, blame, or dump arguments; replacing VSTest@3; and exit code 8 or zero tests. Also use for xUnit v3 MTP filters during a v2-to-v3 upgrade. Do not use for framework conversion, TFM, UWP, or WinUI.

This plugin packages the [`migrate-vstest-to-mtp`](skills/migrate-vstest-to-mtp/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test-migration/skills/migrate-vstest-to-mtp) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/migrate-vstest-to-mtp/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install migrate-vstest-to-mtp@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmigrate-vstest-to-mtp),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `migrate-vstest-to-mtp`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
