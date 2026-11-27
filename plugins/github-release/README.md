# github-release

Guides IA through releasing a new version of a GitHub library end-to-end. Handles SemVer versioning and Keep a Changelog formatting automatically.

This plugin packages the [`github-release`](skills/github-release/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/github-release) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/github-release/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install github-release@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgithub-release),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `github-release`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
