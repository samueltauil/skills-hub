# security-ownership-map

Analyze git repositories to build a security ownership topology (people-to-file), compute bus factor and sensitive-code ownership, and export CSV/JSON for graph databases and visualization. Trigger only when the user explicitly wants a security-oriented ownership or bus-factor analysis grounded in git history (for example: orphaned sensitive code, security maintainers, CODEOWNERS reality checks for risk, sensitive hotspots, or ownership clusters). Do not trigger for general maintainer lists or non-security ownership questions.

This plugin packages the [`security-ownership-map`](skills/security-ownership-map/SKILL.md) skill from
[openai/skills](https://github.com/openai/skills/tree/main/skills/.curated/security-ownership-map) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/security-ownership-map/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install security-ownership-map@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsecurity-ownership-map),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `security-ownership-map`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[openai/skills](https://github.com/openai/skills).
