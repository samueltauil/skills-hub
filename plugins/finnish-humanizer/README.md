# finnish-humanizer

Detect and remove AI-generated markers from Finnish text, making it sound like a native Finnish speaker wrote it. Use when asked to "humanize", "naturalize", or "remove AI feel" from Finnish text, or when editing .md/.txt files containing Finnish content. Identifies 26 patterns (12 Finnish-specific + 14 universal) and 4 style markers.

This plugin packages the [`finnish-humanizer`](skills/finnish-humanizer/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/finnish-humanizer) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/finnish-humanizer/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install finnish-humanizer@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dfinnish-humanizer),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `finnish-humanizer`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
