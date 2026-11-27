# pester-should-migration

Experimental (preview) Pester skill for migrating classic Should -Be (v5) assertion syntax to the new Should-* (v6) assertions (note the hyphen, no space), e.g. `Should -Be` -> `Should-Be`, `Should -Not -Be` -> `Should-NotBe`. Tracks Pester 6, which is still a release candidate, so this guidance may change; verified against Pester 6.0.0-rc2. Use when converting Pester v5 assertions to Pester v6 Should-* operators, modernizing a Pester test suite, or when a user asks to migrate, convert, or rewrite `Should -...` calls in .Tests.ps1 / PowerShell files.

This plugin packages the [`pester-should-migration`](skills/pester-should-migration/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/pester-should-migration) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/pester-should-migration/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install pester-should-migration@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpester-should-migration),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `pester-should-migration`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
