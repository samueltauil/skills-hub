# vardoger-analyze

Use when the user asks to personalize the GitHub Copilot CLI assistant, adapt Copilot to their style, use vardoger, or analyze their Copilot CLI conversation history. Reads the local session directory at `~/.copilot/session-state/`, extracts recurring preferences and conventions, and writes a fenced personalization block into `~/.copilot/copilot-instructions.md`. Runs entirely on the user's machine via the local `vardoger` CLI (`pipx install vardoger`); no network calls and no uploads. Triggers: 'personalize my copilot', 'analyze my copilot history', 'tailor copilot to me', 'run vardoger', 'update my copilot instructions from history', 'make copilot learn my style'.

This plugin packages the [`vardoger-analyze`](skills/vardoger-analyze/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/vardoger-analyze) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/vardoger-analyze/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install vardoger-analyze@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dvardoger-analyze),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `vardoger-analyze`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
