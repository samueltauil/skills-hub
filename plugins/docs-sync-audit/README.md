# docs-sync-audit

Run a read-only documentation drift audit for a feature, PR, branch, release, API, configuration change, workflow, CLI, package, or repository area. Use when the user asks whether docs are stale, missing, inconsistent with code, or need updates after code changes. Checks README files, setup guides, API docs, env docs, changelogs, examples, comments, generated docs, and user-facing instructions. This is not a general code review; it compares what the docs claim against what the code does.

This plugin packages the [`docs-sync-audit`](skills/docs-sync-audit/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/docs-sync-audit) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/docs-sync-audit/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install docs-sync-audit@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddocs-sync-audit),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `docs-sync-audit`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
