# dotnet-maui-doctor

Diagnoses and fixes .NET MAUI development environment issues. Validates .NET SDK, workloads, Java JDK, Android SDK, Xcode, and Windows SDK. All version requirements discovered dynamically from NuGet WorkloadDependencies.json — never hardcoded. Use when: setting up MAUI development, build errors mentioning SDK/workload/JDK/Android, "Android SDK not found", "Java version" errors, "Xcode not found", environment verification after updates, or any MAUI toolchain issues. Do not use for: non-MAUI .NET projects, Xamarin.Forms apps, runtime app crashes unrelated to environment setup, or app store publishing issues. Works on macOS, Windows, and Linux.

This plugin packages the [`dotnet-maui-doctor`](skills/dotnet-maui-doctor/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-maui/skills/dotnet-maui-doctor) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/dotnet-maui-doctor/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install dotnet-maui-doctor@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddotnet-maui-doctor),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `dotnet-maui-doctor`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
