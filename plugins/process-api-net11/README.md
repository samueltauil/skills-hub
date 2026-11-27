# process-api-net11

Launch and supervise executable child processes on .NET 11 or later with System.Diagnostics.Process or SafeProcessHandle. DO NOT USE FOR: opening URLs in the default browser or documents in their associated application. Those are operating-system shell-association requests, not executable child-process management, even on .NET 11. DO NOT USE FOR: projects that must remain on .NET 10 or earlier. USE FOR: launching executables; preventing redirected stdout/stderr pipe deadlocks; capturing text, bytes, or interleaved lines; waiting for exit status; cancellation and timeouts; redirecting standard handles to files, pipes, or the null device; restricting handle inheritance; custom native process creation; fire-and-forget starts; parent-exit termination; terminal detachment; SafeProcessHandle and trimmer-friendly process management for NativeAOT applications.

This plugin packages the [`process-api-net11`](skills/process-api-net11/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet11/skills/process-api-net11) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/process-api-net11/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install process-api-net11@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dprocess-api-net11),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `process-api-net11`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
