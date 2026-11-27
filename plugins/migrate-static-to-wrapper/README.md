# migrate-static-to-wrapper

ALWAYS USE when asked to migrate, replace, or make testable existing C# static calls with a named wrapper or built-in abstraction: DateTime.UtcNow/Now or DateTimeOffset.UtcNow to TimeProvider/IClock, File.* to IFileSystem or an existing store such as ITextFileStore, and Environment.* to an existing reader such as IEnvironmentReader. Covers scoped files/projects, constructor injection, replacing temp-file or process-environment tests with fakes, "already registered" abstractions, and static classes whose callers/signatures must stay unchanged. Preserves DateTimeKind and call count. DO NOT USE for finding statics (detect-static-dependencies), choosing/designing a new wrapper (generate-testability-wrappers), behavior tests with no chosen seam (testability-obstacle), or test-framework migration.

This plugin packages the [`migrate-static-to-wrapper`](skills/migrate-static-to-wrapper/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test/skills/migrate-static-to-wrapper) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/migrate-static-to-wrapper/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install migrate-static-to-wrapper@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmigrate-static-to-wrapper),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `migrate-static-to-wrapper`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
