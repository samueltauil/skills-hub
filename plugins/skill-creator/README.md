# skill-creator

Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.

This plugin packages the [`skill-creator`](skills/skill-creator/SKILL.md) skill from
[anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/skill-creator) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/skill-creator/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install skill-creator@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dskill-creator),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `skill-creator`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[anthropics/skills](https://github.com/anthropics/skills).
