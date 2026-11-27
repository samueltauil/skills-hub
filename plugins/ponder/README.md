# ponder

Convergent deliberation loop - repeated grading passes over one subject until the answer stops changing, with coverage enforced so no unit is silently skipped. Use when the user says "ponder <anything>" ("ponder the UI", "ponder our error handling"), "think this over properly", "keep thinking until it converges", "keep looping until it converges", "loop on this until it stops changing", "go through all the screens and grade them", "audit/rate/grade every X", or asks for any broad sweep-and-grade across many units where a single pass would miss things. Also use to resume or recover a ponder already in flight - "where were we", "carry on pondering", a lost thread mid-loop, or a .ponder/ directory in the project - where the move is to run ponder status rather than start over.

This plugin packages the [`ponder`](skills/ponder/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/ponder) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/ponder/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install ponder@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dponder),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `ponder`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
