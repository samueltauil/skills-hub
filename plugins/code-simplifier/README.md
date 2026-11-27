# code-simplifier

Simplifies and refines code for clarity, consistency, and maintainability while preserving all functionality. Use when asked to "simplify code", "clean up code", "refactor for clarity", "improve readability", or review recently modified code for elegance. Focuses on project-specific best practices.

This plugin packages the [`code-simplifier`](skills/code-simplifier/SKILL.md) skill from
[getsentry/skills](https://github.com/getsentry/skills/tree/main/skills/code-simplifier) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/code-simplifier/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install code-simplifier@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcode-simplifier),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `code-simplifier`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[getsentry/skills](https://github.com/getsentry/skills).
