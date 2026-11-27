# testability-obstacle

MUST USE for C#/.NET deterministic tests that require the smallest production seam for DateTime/Task.Delay/File/Environment/Guid/Random, static API preservation, nested/parallel overrides, or no real I/O. USE ONLY when the target workspace contains C# source plus a .csproj or .sln. DO NOT USE for audits, bulk migration, code that already has an injectable seam, or an explicit migration to a user-named existing abstraction (migrate-static-to-wrapper). Use instead of general test generation when the requested test is impossible without a production edit and seam selection is still open.

This plugin packages the [`testability-obstacle`](skills/testability-obstacle/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test/skills/testability-obstacle) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/testability-obstacle/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install testability-obstacle@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dtestability-obstacle),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `testability-obstacle`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
