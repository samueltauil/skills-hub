# gh-address-comments

Help address review/issue comments on the open GitHub PR for the current branch using gh CLI; verify gh auth first and prompt the user to authenticate if not logged in.

This plugin packages the [`gh-address-comments`](skills/gh-address-comments/SKILL.md) skill from
[openai/skills](https://github.com/openai/skills/tree/main/skills/.curated/gh-address-comments) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gh-address-comments/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gh-address-comments@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgh-address-comments),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gh-address-comments`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[openai/skills](https://github.com/openai/skills).
