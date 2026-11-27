# extension-to-functions-codebase

Skill for converting an installed Firebase Extension (or extension source) into a standalone Cloud Functions for Firebase codebase or publishable npm package, including V1 to V2 trigger upgrades, lifecycle hooks, and declarative security

This plugin packages the [`extension-to-functions-codebase`](skills/extension-to-functions-codebase/SKILL.md) skill from
[firebase/agent-skills](https://github.com/firebase/agent-skills/tree/main/skills/extension-to-functions-codebase) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/extension-to-functions-codebase/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install extension-to-functions-codebase@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dextension-to-functions-codebase),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `extension-to-functions-codebase`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[firebase/agent-skills](https://github.com/firebase/agent-skills).
