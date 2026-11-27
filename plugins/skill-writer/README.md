# skill-writer

Create, synthesize, and iteratively improve agent skills following the Agent Skills specification. Use when asked to "create a skill", "write a skill", "synthesize sources into a skill", "improve a skill from positive/negative examples", "update a skill", or "maintain skill docs and registration". Handles source capture, precision passes, authoring, registration, and validation.

This plugin packages the [`skill-writer`](skills/skill-writer/SKILL.md) skill from
[getsentry/skills](https://github.com/getsentry/skills/tree/main/skills/skill-writer) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/skill-writer/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install skill-writer@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dskill-writer),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `skill-writer`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[getsentry/skills](https://github.com/getsentry/skills).
