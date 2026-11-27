# bench-read

Read artifacts from the shared bench — the workspace where desks leave findings, verdicts, and work products for each other and the operator.

This plugin packages the [`bench-read`](skills/bench-read/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/bench-read) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/bench-read/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install bench-read@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dbench-read),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `bench-read`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
