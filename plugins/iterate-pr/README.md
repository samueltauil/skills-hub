# iterate-pr

Iterate on a PR until actionable CI passes and high/medium review feedback is addressed. Use for PR CI failures, review feedback, or green-check loops; do not wait for human approval, draft status, or merge gates.

This plugin packages the [`iterate-pr`](skills/iterate-pr/SKILL.md) skill from
[getsentry/skills](https://github.com/getsentry/skills/tree/main/skills/iterate-pr) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/iterate-pr/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install iterate-pr@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Diterate-pr),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `iterate-pr`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[getsentry/skills](https://github.com/getsentry/skills).
