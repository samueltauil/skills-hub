# poka-yoke

Mistake-proof code so misuse cannot be expressed, rather than warning against it. Use when designing an interface, schema, or state machine and the user wants it hard to get wrong ("make invalid states unrepresentable", "so callers cannot screw it up", "type-safe API", "pit of success"); when auditing existing code for footguns ("what could bite us here", "what is easy to misuse", "poka-yoke this repo", "review this diff for ways to get it wrong"); or when a bug has recurred and the fix must close the class rather than the case ("make sure this never happens again", "this is the third time"). Especially for money, auth, permissions, deletion, migrations, and pipelines where failure is silent. Classifies every finding by what happens when the mistake occurs and how the device notices, which is what keeps it from collapsing into generic code review.

This plugin packages the [`poka-yoke`](skills/poka-yoke/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/poka-yoke) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/poka-yoke/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install poka-yoke@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpoka-yoke),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `poka-yoke`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
