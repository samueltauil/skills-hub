# threat-model-analyst

Full STRIDE-A threat model analysis and incremental update skill for repositories and systems. Supports two modes: (1) Single analysis — full STRIDE-A threat model of a repository, producing architecture overviews, DFD diagrams, STRIDE-A analysis, prioritized findings, and executive assessments. (2) Incremental analysis — takes a previous threat model report as baseline, compares the codebase at the latest (or a given commit), and produces an updated report with change tracking (new, resolved, still-present threats), STRIDE heatmap, findings diff, and an embedded HTML comparison. Only activate when the user explicitly requests a threat model analysis, incremental update, or invokes /threat-model-analyst directly.

This plugin packages the [`threat-model-analyst`](skills/threat-model-analyst/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/threat-model-analyst) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/threat-model-analyst/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install threat-model-analyst@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dthreat-model-analyst),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `threat-model-analyst`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
