# clr-activation-debugging

Diagnoses .NET Framework CLR activation issues using CLR activation logs (CLRLoad logs) produced by mscoree.dll. Use when: the shim picks the wrong runtime, fails to load any runtime, shows unexpected .NET 3.5 Feature-on-Demand (FOD) dialogs, unexpectedly does NOT show FOD dialogs, loads both v2 and v4 into the same process causing failures, or any time someone is wondering "what is happening with .NET Framework activation?"

This plugin packages the [`clr-activation-debugging`](skills/clr-activation-debugging/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-diag/skills/clr-activation-debugging) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/clr-activation-debugging/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install clr-activation-debugging@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dclr-activation-debugging),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `clr-activation-debugging`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
