# firebase-firestore

Sets up, manages, queries, and configures Cloud Firestore databases (Standard/Enterprise edition), including data modeling, security rules, indexes, and SDK integrations (Web, Admin, Python, iOS, Android, Flutter). Use when adding or migrating app databases, creating/listing Firestore databases, defining data models/indexes, writing SDK queries, or integrating Firestore SDKs. For authoring or modifying Firestore Security Rules (firestore.rules), delegate to the firestore-rules-author subagent if subagent delegation is available, or use firestore-rules-creation otherwise. Don't use for Data Connect, BigQuery, or standalone Hosting, Auth, Storage/GCS, Crashlytics, or Functions tasks.

This plugin packages the [`firebase-firestore`](skills/firebase-firestore/SKILL.md) skill from
[firebase/agent-skills](https://github.com/firebase/agent-skills/tree/main/skills/firebase-firestore) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/firebase-firestore/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install firebase-firestore@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dfirebase-firestore),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `firebase-firestore`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[firebase/agent-skills](https://github.com/firebase/agent-skills).
