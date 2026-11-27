# pr-artifact-explorer

Open, share, and inspect GitHub PRs, issues, workflow runs (including scheduled, manual and other runs with no PR), Actions artifacts, and local or HTTP(S) web previews in the Artifact Explorer canvas, with viewport presets, zoom, screenshots, and recoverable download jobs.

This plugin packages the [`pr-artifact-explorer`](skills/pr-artifact-explorer/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/pr-artifact-explorer) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/pr-artifact-explorer/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install pr-artifact-explorer@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpr-artifact-explorer),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `pr-artifact-explorer`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
