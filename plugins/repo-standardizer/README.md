# repo-standardizer

Polish any GitHub repository's surface — labels (emoji rating tiers, P0–P3 priority, impact severity), issue forms, PR template, CI workflows, CODEOWNERS, rulesets, docs. Repo meta & config only — no code logic touched. Use when creating a new repo or polishing an existing one.

This plugin packages the [`repo-standardizer`](skills/repo-standardizer/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/repo-standardizer) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/repo-standardizer/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install repo-standardizer@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Drepo-standardizer),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `repo-standardizer`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
