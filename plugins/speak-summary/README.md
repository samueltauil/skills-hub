# speak-summary

Convert text, markdown, or a summary produced by another skill into a listenable MP3 using local CPU-only neural text-to-speech. Rewrites written prose for the ear before synthesising. Use when the user asks to "read this out", "turn this into audio", "make an MP3", "I want to listen to this", "podcast version", or wants a spoken digest for a commute or breakfast.

This plugin packages the [`speak-summary`](skills/speak-summary/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/speak-summary) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/speak-summary/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install speak-summary@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dspeak-summary),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `speak-summary`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
