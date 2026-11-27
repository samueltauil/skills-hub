# scout-issue

Use when a developer wants to find the best GitHub issues to contribute to in a repository. Invoke with /scout-issue or ask to find good first issues, beginner-friendly issues, or open source work. Asks about experience level, technical skills, time, and contribution type, then searches GitHub issues, scores them, and presents ranked recommendations with match analysis.

This plugin packages the [`scout-issue`](skills/scout-issue/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/scout-issue) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/scout-issue/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install scout-issue@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dscout-issue),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `scout-issue`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
