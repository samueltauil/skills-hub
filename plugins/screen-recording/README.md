# screen-recording

Create annotated animated GIF demos and screen recordings for pull requests and documentation. Covers frame capture, timing, imageio-based GIF creation, and per-frame annotation workflows.

This plugin packages the [`screen-recording`](skills/screen-recording/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/screen-recording) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/screen-recording/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install screen-recording@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dscreen-recording),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `screen-recording`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
