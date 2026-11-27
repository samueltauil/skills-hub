# writing-user-docs

House style for user-facing documentation — voice, scope, structure, and what to leave out. Use this skill whenever writing, editing, or reviewing anything a user reads to learn how to use a tool — help center articles, getting-started guides, tutorials, feature docs, README usage sections, in-app help, release notes, or FAQ entries. Trigger it even when the request is phrased plainly — "document this feature", "write docs for X", "explain this to users", "write a README for this library", "turn these notes into a guide" — and even when no style guidelines are mentioned. Also use it to review existing docs for tone, bloat, or leaked implementation detail. Do not use it for internal engineering docs, architecture write-ups, RFCs, or code comments.

This plugin packages the [`writing-user-docs`](skills/writing-user-docs/SKILL.md) skill from
[callstackincubator/agent-skills](https://github.com/callstackincubator/agent-skills/tree/main/skills/writing-user-docs) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/writing-user-docs/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install writing-user-docs@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dwriting-user-docs),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `writing-user-docs`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[callstackincubator/agent-skills](https://github.com/callstackincubator/agent-skills).
