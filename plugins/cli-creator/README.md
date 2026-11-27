# cli-creator

Build a composable CLI for Codex from API docs, an OpenAPI spec, existing curl examples, an SDK, a web app, an admin tool, or a local script. Use when the user wants Codex to create a command-line tool that can run from any repo, expose composable read/write commands, return stable JSON, manage auth, and pair with a companion skill.

This plugin packages the [`cli-creator`](skills/cli-creator/SKILL.md) skill from
[openai/skills](https://github.com/openai/skills/tree/main/skills/.curated/cli-creator) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/cli-creator/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install cli-creator@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcli-creator),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `cli-creator`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[openai/skills](https://github.com/openai/skills).
