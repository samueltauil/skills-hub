# gitmoji

Generates commit messages following the gitmoji convention (https://gitmoji.dev) — picks the right emoji for the intent of the change and writes a well-formed message. Use when asked to "write a gitmoji commit", "add an emoji to my commit message", "which gitmoji should I use", "gitmoji this change", or when a project uses gitmoji-style commit messages. Works from a git diff, staged changes, or a plain description of the change. Generates the message only — does not run git commands.

This plugin packages the [`gitmoji`](skills/gitmoji/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/gitmoji) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gitmoji/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gitmoji@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgitmoji),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gitmoji`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
