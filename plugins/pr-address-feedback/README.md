# pr-address-feedback

Walk through PR review comments one-by-one, deciding for each whether to act on the feedback or reply with reasoning, and build an approvable resolution plan before changing anything. Use when the user wants to address, respond to, or triage PR review feedback.

This plugin packages the [`pr-address-feedback`](skills/pr-address-feedback/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/pr-address-feedback) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/pr-address-feedback/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install pr-address-feedback@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpr-address-feedback),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `pr-address-feedback`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
