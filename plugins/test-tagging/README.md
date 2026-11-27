# test-tagging

Classifies existing tests by standard traits and reports their distribution. USE FOR: tagging all tests with category attributes, categorizing/tagging/ labeling each test, compare happy vs error paths, audit the test mix, describe coverage shape by test type, or tag then verify the project builds. Read bodies when names mislead. Apply canonical attributes; otherwise report only. DO NOT USE FOR: requests owned by test-anti-patterns, coverage-analysis, crap-score, test-gap-analysis, code-testing, or migration skills.

This plugin packages the [`test-tagging`](skills/test-tagging/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test/skills/test-tagging) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/test-tagging/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install test-tagging@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dtest-tagging),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `test-tagging`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
