# test-gap-analysis

Find caller-visible production changes existing tests would miss through pseudo-mutation analysis; verify candidates or close gaps only when requested. Includes read-only per-test composition for grading. Polyglot. USE FOR: would tests catch a bug, behavioral blind spots, surviving mutations. DO NOT USE FOR: concrete fix/feature revision proof (test-value-evidence); suite taxonomy (test-tagging); .NET coverage, Cobertura, plateaus or coverage-backed priorities (coverage-analysis); named CRAP (crap-score); new suites (code-testing); assertion/smell audits; mutation tools.

This plugin packages the [`test-gap-analysis`](skills/test-gap-analysis/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-test/skills/test-gap-analysis) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/test-gap-analysis/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install test-gap-analysis@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dtest-gap-analysis),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `test-gap-analysis`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
