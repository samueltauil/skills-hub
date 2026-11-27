# setup-my-iq

Create, set up, or update the personal context portfolio: structured markdown files describing who you are, how you work, your teams, and your tool/ADO configuration. Runs the interview workflow for first-time setup and targeted edits for updates. Trigger this skill when the user asks to: set up their context, create or update their context portfolio, "create my IQ", "set up my IQ", edit their profile, add/remove a stakeholder, update ADO config, change team info, update pillars, or set up any plugin configuration. Trigger when another skill fails to find context (missing files or TODO markers) and needs context populated. Also trigger when the user mentions a context change in passing (e.g., "my manager changed", "we added someone to the team") to offer a context file update. Do NOT trigger for read-only questions like "who's on my team?" or "what's my ADO config?". Those are answered directly from the context files referenced in the loaded custom instructions; no skill is needed.

This plugin packages the [`setup-my-iq`](skills/setup-my-iq/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/setup-my-iq) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/setup-my-iq/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install setup-my-iq@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsetup-my-iq),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `setup-my-iq`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
