# steno-mode

Shorthand-first response compression that cuts ~40% of response tokens while preserving technical precision and exact literals. Use when the user says "steno mode", "shorthand mode", "compressed responses", "token reduction", "brief structured output", or invokes /steno. Supports four compression levels: lite, brief, court, machine. Do not trigger for requests needing polished prose such as onboarding/tutorial content, stakeholder or customer-facing copy, or teaching-focused explanations.

This plugin packages the [`steno-mode`](skills/steno-mode/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/steno-mode) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/steno-mode/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install steno-mode@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsteno-mode),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `steno-mode`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
