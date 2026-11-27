# workshop-create

Create a new workshop or use an existing directory as one. Handles two paths: (A) use an existing local directory the operator points at, or (B) create a new private GitHub repo in the signed-in account. Never creates a repo inside another repo.

This plugin packages the [`workshop-create`](skills/workshop-create/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/workshop-create) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/workshop-create/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install workshop-create@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dworkshop-create),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `workshop-create`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
