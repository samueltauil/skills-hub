# firebase-data-connect-basics

Builds and deploys Firebase SQL Connect (aka Firebase Data Connect) backends with PostgreSQL securely. Use when designing schemas with tables and relations, writing authorized queries and mutations, configuring real-time data updates, or generating type-safe SDKs. Use when you need a relational database with Firebase, or when the user mentions SQL Connect or Data Connect.

This plugin packages the [`firebase-data-connect`](skills/firebase-data-connect/SKILL.md) skill from
[firebase/agent-skills](https://github.com/firebase/agent-skills/tree/main/skills/firebase-data-connect-basics) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/firebase-data-connect-basics/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install firebase-data-connect-basics@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dfirebase-data-connect-basics),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `firebase-data-connect-basics`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[firebase/agent-skills](https://github.com/firebase/agent-skills).
