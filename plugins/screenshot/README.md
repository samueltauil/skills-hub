# screenshot

Use when the user explicitly asks for a desktop or system screenshot (full screen, specific app or window, or a pixel region), or when tool-specific capture capabilities are unavailable and an OS-level capture is needed.

This plugin packages the [`screenshot`](skills/screenshot/SKILL.md) skill from
[openai/skills](https://github.com/openai/skills/tree/main/skills/.curated/screenshot) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/screenshot/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install screenshot@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dscreenshot),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `screenshot`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[openai/skills](https://github.com/openai/skills).
