# pr-link-issue

Append a GitHub issue link and its Linear ticket to the current PR's description. Use when asked to "link issue to pr", "fill in issue and linear in pr", "add issue refs to pr", or when given a GitHub issue URL and asked to attach it to the current PR. Resolves the Linear ticket automatically from the issue's linear-linkback comment.

This plugin packages the [`pr-link-issue`](skills/pr-link-issue/SKILL.md) skill from
[getsentry/skills](https://github.com/getsentry/skills/tree/main/skills/pr-link-issue) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/pr-link-issue/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install pr-link-issue@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpr-link-issue),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `pr-link-issue`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[getsentry/skills](https://github.com/getsentry/skills).
