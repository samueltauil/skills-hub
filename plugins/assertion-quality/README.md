# assertion-quality

Analyze weak, shallow, trivial, self-referential, assertion-free, or presence-only assertions; Contains fragments or totals replacing predictable generated code, JSON, CLI, report, or protocol output. Supports MSTest, Jest, pytest, and Go. DO NOT USE for direct assertion fixes (writing-mstest-tests for MSTest, code-testing for other frameworks), new cases (code-testing), missing scenarios or identified production changes (test-gap-analysis), or general severity-ranked audits (test-anti-patterns).

This plugin packages the [`assertion-quality`](skills/assertion-quality/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test/skills/assertion-quality) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/assertion-quality/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install assertion-quality@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dassertion-quality),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `assertion-quality`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
