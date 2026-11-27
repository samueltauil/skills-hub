# dependabot

Comprehensive guide for configuring and managing GitHub Dependabot. Use this skill when users ask about creating or optimizing dependabot.yml files, managing Dependabot pull requests, configuring dependency update strategies, setting up grouped updates, monorepo patterns, multi-ecosystem groups, security update configuration, auto-triage rules, or any GitHub Advanced Security (GHAS) supply chain security topic related to Dependabot. For pre-commit dependency vulnerability scanning in AI coding agents via the GitHub MCP Server, this skill references the Advanced Security plugin (`advanced-security@copilot-plugins`). Use this skill when an agent needs to scan dependencies for known vulnerabilities before committing.

This plugin packages the [`dependabot`](skills/dependabot/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/dependabot) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/dependabot/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install dependabot@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddependabot),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `dependabot`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
