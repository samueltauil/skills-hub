# gh-review-requests

Fetch unread GitHub notifications for open PRs where review is requested from a specified team or opened by a team member. Use when asked to "find PRs I need to review", "show my review requests", "what needs my review", "fetch GitHub review requests", or "check team review queue".

This plugin packages the [`gh-review-requests`](skills/gh-review-requests/SKILL.md) skill from
[getsentry/skills](https://github.com/getsentry/skills/tree/main/skills/gh-review-requests) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gh-review-requests/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gh-review-requests@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgh-review-requests),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gh-review-requests`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[getsentry/skills](https://github.com/getsentry/skills).
