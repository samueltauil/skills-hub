# copilot-cli-quickstart

Use this skill when someone wants to learn GitHub Copilot CLI from scratch. Offers interactive step-by-step tutorials with separate Developer and Non-Developer tracks, plus on-demand Q&A. Just say "start tutorial" or ask a question! Note: This skill targets GitHub Copilot CLI specifically and uses CLI-specific tools (ask_user, sql, fetch_copilot_cli_documentation).

This plugin packages the [`copilot-cli-quickstart`](skills/copilot-cli-quickstart/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/copilot-cli-quickstart) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/copilot-cli-quickstart/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install copilot-cli-quickstart@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcopilot-cli-quickstart),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `copilot-cli-quickstart`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
