# migrate-xunit-to-xunit-v3

Migrate .NET test projects from xUnit.net v2 to xunit.v3 and fix v3 breaks. Use for package/CPM conversion, OutputType=Exe, preserving the VSTest or MTP runner (including projects currently using YTest.MTP.XUnit2), incompatible TFMs, async void tests, string-to-Type attributes, custom Fact/Theory/BeforeAfterTest attributes, Xunit.SkippableFact, xunit.abstractions/extensibility consolidation, and Xunit.Combinatorial/StaFact compatibility. Do not use for framework conversion or a runner-only migration. For xUnit v3 MTP filter syntax, also use migrate-vstest-to-mtp.

This plugin packages the [`migrate-xunit-to-xunit-v3`](skills/migrate-xunit-to-xunit-v3/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test-migration/skills/migrate-xunit-to-xunit-v3) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/migrate-xunit-to-xunit-v3/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install migrate-xunit-to-xunit-v3@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmigrate-xunit-to-xunit-v3),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `migrate-xunit-to-xunit-v3`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
