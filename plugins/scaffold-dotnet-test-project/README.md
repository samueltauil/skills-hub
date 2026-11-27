# scaffold-dotnet-test-project

MUST USE when an existing .NET test project was excluded from a .slnf/CI solution filter, disappeared from .sln/.slnx discovery, or lost its production ProjectReference; also for requests to set up, create, reuse, add, register, include, or repair a test project. Handles "tests pass directly but CI discovers zero", exact solution wiring, xUnit/NUnit/MSTest, and central packages. DO NOT USE to only author tests in an already-wired project (code-testing), run tests, migrate, or correct MSTest syntax/configuration without changing project or CI files (writing-mstest-tests).

This plugin packages the [`scaffold-dotnet-test-project`](skills/scaffold-dotnet-test-project/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test/skills/scaffold-dotnet-test-project) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/scaffold-dotnet-test-project/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install scaffold-dotnet-test-project@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dscaffold-dotnet-test-project),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `scaffold-dotnet-test-project`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
