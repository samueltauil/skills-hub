# pr-dashboard

Open a GitHub PR dashboard in the browser. Use when the user asks to see their pull requests, open the PR dashboard, show PRs for a date range, or check PR status. Trigger phrases include "show my PRs", "open PR dashboard", "pull request dashboard".

This plugin packages the [`pr-dashboard`](skills/pr-dashboard/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/pr-dashboard) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/pr-dashboard/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install pr-dashboard@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpr-dashboard),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `pr-dashboard`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
