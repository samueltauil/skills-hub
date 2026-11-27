# refactor

Surgical code refactoring to improve maintainability without changing behavior. Covers extracting functions, renaming variables, breaking down god functions, improving type safety, eliminating code smells, and applying design patterns. Less drastic than repo-rebuilder; use for gradual improvements.

This plugin packages the [`refactor`](skills/refactor/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/refactor) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/refactor/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install refactor@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Drefactor),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `refactor`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
