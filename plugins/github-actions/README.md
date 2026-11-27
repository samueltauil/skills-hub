# github-actions

GitHub Actions workflow patterns for React Native iOS simulator and Android emulator cloud builds with downloadable artifacts. Use when setting up CI build pipelines or downloading GitHub Actions artifacts via gh CLI and GitHub API.

This plugin packages the [`github-actions`](skills/github-actions/SKILL.md) skill from
[callstackincubator/agent-skills](https://github.com/callstackincubator/agent-skills/tree/main/skills/github-actions) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/github-actions/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install github-actions@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgithub-actions),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `github-actions`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[callstackincubator/agent-skills](https://github.com/callstackincubator/agent-skills).
