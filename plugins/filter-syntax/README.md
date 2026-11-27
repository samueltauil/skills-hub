# filter-syntax

Reference-only filter syntax for VSTest and MTP with MSTest, NUnit, xUnit v3, and TUnit. Load only after the platform/framework is known and a consumer needs to create or translate a filter. Do not load for unfiltered runs or platform detection. Used by run-tests and mtp-hot-reload; never invoke directly.

This plugin packages the [`filter-syntax`](skills/filter-syntax/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test/skills/filter-syntax) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/filter-syntax/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install filter-syntax@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dfilter-syntax),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `filter-syntax`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
