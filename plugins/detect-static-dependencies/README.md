# detect-static-dependencies

ACTIVATION PREREQUISITE: the request or discovered target must explicitly identify C#, .NET, `.cs`, or `.csproj`; otherwise stay dormant without invoking this skill. USE FOR: locating System.DateTime.Now/UtcNow, System.IO.File/Directory, System.Environment, HttpClient, Console, or Process usage in C#; auditing C# code for hard-to-test framework dependencies; or verifying those C# calls are already abstracted. DO NOT USE FOR: any target lacking the activation prerequisite; generating wrappers (use generate-testability-wrappers); migrating code (use migrate-static-to-wrapper); or general code review.

This plugin packages the [`detect-static-dependencies`](skills/detect-static-dependencies/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test/skills/detect-static-dependencies) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/detect-static-dependencies/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install detect-static-dependencies@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddetect-static-dependencies),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `detect-static-dependencies`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
