# thread-abort-migration

Guides migration of .NET Framework Thread.Abort usage to cooperative cancellation in modern .NET. USE FOR: modernizing code that calls Thread.Abort, catching ThreadAbortException, replacing Thread.ResetAbort, replacing Thread.Interrupt for thread termination, resolving PlatformNotSupportedException or SYSLIB0006 after retargeting to .NET 6+, migrating ASP.NET Response.End or Response.Redirect(url, true) which internally call Thread.Abort. DO NOT USE FOR: code that only uses Thread.Join, Thread.Sleep, or Thread.Start without any abort, interrupt, or ThreadAbortException usage — these APIs work identically in modern .NET and need no migration. Also not for projects staying on .NET Framework, or Thread.Abort usage inside third-party libraries you do not control.

This plugin packages the [`thread-abort-migration`](skills/thread-abort-migration/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-upgrade/skills/thread-abort-migration) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/thread-abort-migration/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install thread-abort-migration@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dthread-abort-migration),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `thread-abort-migration`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
