# run-tests

ALWAYS USE before running .NET tests or answering with a test command or flags. Trigger on "run the tests", "exact dotnet test command", one test/class/category/trait/target framework, combined filters, `--filter-query`, `--no-build`, `--diag`, diagnostic logs, TRX, coverage collection, crash/hang dumps, filter errors, or unrecognized options. Chooses repository-compatible classic, VSTest, bridged MTP, or native MTP syntax for MSTest/xUnit/NUnit/TUnit. DO NOT USE for platform identification alone (platform-detection), writing or debugging test code, interpreting an existing coverage report, CI investigation, migration, or a persistent hot reload/watch loop.

This plugin packages the [`run-tests`](skills/run-tests/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test/skills/run-tests) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/run-tests/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install run-tests@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Drun-tests),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `run-tests`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
