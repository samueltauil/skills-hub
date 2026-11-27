# crap-score

Calculates CRAP (Change Risk Anti-Patterns) for a named .NET method, class, or file. USE FOR: explicit CRAP calculation or coverage-and-complexity risk within that named target, including which tests to prioritize. DO NOT USE FOR: project-wide coverage/CRAP, plateaus, or project-wide blockers/priorities (coverage-analysis); behavioral/pseudo-mutation gaps (test-gap-analysis); writing tests; test runs without CRAP context.

This plugin packages the [`crap-score`](skills/crap-score/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test/skills/crap-score) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/crap-score/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install crap-score@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcrap-score),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `crap-score`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
