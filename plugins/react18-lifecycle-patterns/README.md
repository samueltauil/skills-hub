# react18-lifecycle-patterns

Provides exact before/after migration patterns for the three unsafe class component lifecycle methods - componentWillMount, componentWillReceiveProps, and componentWillUpdate - targeting React 18.3.1. Use this skill whenever a class component needs its lifecycle methods migrated, when deciding between getDerivedStateFromProps vs componentDidUpdate, when adding getSnapshotBeforeUpdate, or when fixing React 18 UNSAFE_ lifecycle warnings. Always use this skill before writing any lifecycle migration code - do not guess the pattern from memory, the decision trees here prevent the most common migration mistakes.

This plugin packages the [`react18-lifecycle-patterns`](skills/react18-lifecycle-patterns/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/react18-lifecycle-patterns) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/react18-lifecycle-patterns/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install react18-lifecycle-patterns@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dreact18-lifecycle-patterns),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `react18-lifecycle-patterns`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
