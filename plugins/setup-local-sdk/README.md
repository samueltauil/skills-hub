# setup-local-sdk

Install a .NET SDK locally for safe preview testing, specific-version pinning, or reproducible team setups — without modifying the system-wide installation. USE FOR: trying .NET previews safely, testing specific SDK versions, installing MAUI or other workloads on a preview, updating or replacing an existing local SDK, creating reproducible team/CI install scripts, configuring global.json paths. DO NOT USE FOR: system-wide SDK installs, .NET hosts older than 10, runtime-only installs, or projects not using SDK-style commands.

This plugin packages the [`setup-local-sdk`](skills/setup-local-sdk/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet/skills/setup-local-sdk) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/setup-local-sdk/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install setup-local-sdk@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsetup-local-sdk),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `setup-local-sdk`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
