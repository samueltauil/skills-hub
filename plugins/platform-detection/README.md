# platform-detection

Identify a .NET project's test platform, framework, command mode, and SDK-style vs classic project system. Use only for "which test platform/framework?", "VSTest or MTP?", or "what runner does this project use?", including bridge settings, UseVSTest opt-outs, and incompatible or conflicting VSTest/MTP configuration. Resolves global.json, project, packages.config, Directory.Build.props, and Directory.Packages.props precedence for MSTest/xUnit/NUnit/TUnit. DO NOT USE when the user asks to run/filter tests or for commands, flags, TRX/dumps, or test-command/filter errors; use run-tests directly. Do not route hot-reload or migration requests here as the entry skill; mtp-hot-reload may use this skill internally for platform detection.

This plugin packages the [`platform-detection`](skills/platform-detection/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test/skills/platform-detection) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/platform-detection/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install platform-detection@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dplatform-detection),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `platform-detection`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
