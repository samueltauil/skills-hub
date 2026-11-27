# coverage-analysis

Activation requires either supplied .NET coverage reports/percentages/line, branch, or condition metrics, or an explicit request to collect .NET coverage for analysis. USE FOR: interpreting that evidence, including Cobertura data, partial conditions, plateaus, target arithmetic, project-wide coverage-backed CRAP, and coverage-backed refactoring safety. Analyze supplied reports directly without rerunning tests or installing tools. DO NOT USE FOR: requests with neither coverage evidence nor explicit coverage-collection intent, including hypothetical change-survival questions (use test-gap-analysis); CRAP or refactoring safety for one named target (use crap-score); or requests owned by test-tagging, find-untested-sources, test-anti-patterns, run-tests, or code-testing.

This plugin packages the [`coverage-analysis`](skills/coverage-analysis/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test/skills/coverage-analysis) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/coverage-analysis/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install coverage-analysis@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcoverage-analysis),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `coverage-analysis`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
