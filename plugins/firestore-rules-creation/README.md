# firestore-rules-creation

Designs, authors, refactors, and hardens production-grade Cloud Firestore Security Rules (firestore.rules). IMPORTANT: If subagent delegation AND the firestore-rules-author subagent are available in your environment, delegate authoring firestore.rules to the firestore-rules-author subagent. If subagent delegation is unavailable (e.g. not enabled in the IDE), firestore-rules-author is not installed, or you are running inside firestore-rules-author, follow this skill directly.

This plugin packages the [`firestore-rules-creation`](skills/firestore-rules-creation/SKILL.md) skill from
[firebase/agent-skills](https://github.com/firebase/agent-skills/tree/main/skills/firestore-rules-creation) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/firestore-rules-creation/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install firestore-rules-creation@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dfirestore-rules-creation),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `firestore-rules-creation`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[firebase/agent-skills](https://github.com/firebase/agent-skills).
