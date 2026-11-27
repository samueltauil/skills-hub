# pester-migration

Pester migration skill for upgrading PowerShell Pester test suites across major versions — v3→v4, v4→v5, and v5→v6. Covers the Discovery/Run two-phase model, moving setup into BeforeAll, $PSScriptRoot vs $MyInvocation, mock changes (Assert-MockCalled → Should -Invoke, removed fall-through), Invoke-Pester parameters → PesterConfiguration, data-driven -ForEach/-TestCases, and the v6 breaking changes. Use when the user asks to upgrade, migrate, or modernize Pester tests, fix *.Tests.ps1 files that broke after bumping the Pester version, or convert legacy Should / Invoke-Pester syntax.

This plugin packages the [`pester-migration`](skills/pester-migration/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/pester-migration) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/pester-migration/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install pester-migration@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpester-migration),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `pester-migration`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
