# commit

Use for every request to commit changes or draft a commit message. Creates Sentry-style conventional commits with issue references.

This plugin packages the [`commit`](skills/commit/SKILL.md) skill from
[getsentry/skills](https://github.com/getsentry/skills/tree/main/skills/commit) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/commit/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install commit@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcommit),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `commit`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[getsentry/skills](https://github.com/getsentry/skills).
