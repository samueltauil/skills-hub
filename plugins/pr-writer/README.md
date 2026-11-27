# pr-writer

Create or refresh reviewer-facing PR titles and descriptions. Use when opening a PR, updating its title or body, or preparing branch changes for review.

This plugin packages the [`pr-writer`](skills/pr-writer/SKILL.md) skill from
[getsentry/skills](https://github.com/getsentry/skills/tree/main/skills/pr-writer) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/pr-writer/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install pr-writer@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpr-writer),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `pr-writer`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[getsentry/skills](https://github.com/getsentry/skills).
