# agents-md

Creates and maintains concise AGENTS.md and CLAUDE.md project instruction files. Use when asked to create AGENTS.md, update AGENTS.md, maintain agent docs, set up CLAUDE.md, document repository agent conventions, or keep coding-agent instructions minimal and reference-backed.

This plugin packages the [`agents-md`](skills/agents-md/SKILL.md) skill from
[getsentry/skills](https://github.com/getsentry/skills/tree/main/skills/agents-md) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/agents-md/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install agents-md@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dagents-md),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `agents-md`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[getsentry/skills](https://github.com/getsentry/skills).
