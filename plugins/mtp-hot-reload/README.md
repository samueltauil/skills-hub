# mtp-hot-reload

Set up or recover MTP hot reload for a long-lived console-host edit/re-run loop in a Microsoft Testing Platform project. Use for explicit MTP console requests such as "enable hot reload", "dotnet run to rerun on edit", or unsupported/rude edits. Covers setup, run/watch, restarts, filters, and the VSTest no-mutation fallback. For one-time runs, exact commands, filter errors, TRX/dumps, or merely a failing test, use run-tests. Do not use when Test Explorer or an IDE should rerun tests without an MTP console host. Excludes editor integration, CI, and writing/debugging tests.

This plugin packages the [`mtp-hot-reload`](skills/mtp-hot-reload/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test/skills/mtp-hot-reload) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/mtp-hot-reload/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install mtp-hot-reload@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmtp-hot-reload),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `mtp-hot-reload`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
