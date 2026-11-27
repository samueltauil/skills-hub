# code-testing-agent

Legacy compatibility alias for the code-testing skill. Do not self-activate for user requests and do not treat this name as a custom agent. When invoked explicitly by older instructions, load code-testing and follow it instead.

This plugin packages the [`code-testing-agent`](skills/code-testing-agent/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test/skills/code-testing-agent) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/code-testing-agent/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install code-testing-agent@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcode-testing-agent),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `code-testing-agent`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
