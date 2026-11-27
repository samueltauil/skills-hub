# drawio

Generate draw.io diagrams as .drawio files and export to PNG/SVG/PDF with embedded XML

This plugin packages the [`drawio`](skills/drawio/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/drawio) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/drawio/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install drawio@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddrawio),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `drawio`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
