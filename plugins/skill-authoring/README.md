# skill-authoring

Author, audit, and improve Grafana SKILL.md files against Anthropic's published Agent Skills guidance and the four-dimension rubric the grafana/skills CI gate uses (conciseness, actionability, workflow clarity, progressive disclosure). Applies the canonical SKILL.md structure (YAML frontmatter + body + references/ + scripts/ + assets/), the "pushy description" trigger pattern, the three-level progressive-disclosure model, and the validate-fix-rerun feedback loop. Use when creating a new skill in this repo, when reviewing a skill PR, when a skill's Tessl review score is below 75 (the merge gate), when a skill's description isn't getting picked up by agents, when restructuring a long SKILL.md into a bundle, or when the user asks how to write, improve, optimize, audit, or fix a skill - even if they don't say "skill" explicitly (e.g. "this isn't triggering", "Tessl scored this 72", "split this doc").

This plugin packages the [`skill-authoring`](skills/skill-authoring/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-core/skill-authoring) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/skill-authoring/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install skill-authoring@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dskill-authoring),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `skill-authoring`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
