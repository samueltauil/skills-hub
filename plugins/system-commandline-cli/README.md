# system-commandline-cli

Use this skill when adding, modifying, or reviewing CLI commands in a .NET project built with System.CommandLine. Triggers include: creating a new CLI command, adding options or arguments, wiring command handlers, registering subcommands, building command groups, or any architecture decision about CLI command structure. Also use when the user mentions 'System.CommandLine', 'CommandBase', 'SetAction', 'ParseResult', 'RootCommand', 'subcommand', or asks to add a verb to the CLI. Do NOT use for general C# coding, web APIs, UI work, or non-CLI projects.

This plugin packages the [`system-commandline-cli`](skills/system-commandline-cli/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/system-commandline-cli) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/system-commandline-cli/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install system-commandline-cli@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsystem-commandline-cli),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `system-commandline-cli`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
