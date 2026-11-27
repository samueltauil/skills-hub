# firebase-remote-config-basics

Manages Firebase Remote Config templates, feature flags, loading strategies, and SDKs (Android, iOS). Use when downloading/deploying remoteconfig JSON templates, managing version history/feature flags, setting in-app defaults, fetchAndActivate(), real-time listeners, or SDK setup. Don't use for Firebase Hosting, Auth, Firestore, Data Connect, Crashlytics, or App Hosting.

This plugin packages the [`firebase-remote-config-basics`](skills/firebase-remote-config-basics/SKILL.md) skill from
[firebase/agent-skills](https://github.com/firebase/agent-skills/tree/main/skills/firebase-remote-config-basics) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/firebase-remote-config-basics/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install firebase-remote-config-basics@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dfirebase-remote-config-basics),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `firebase-remote-config-basics`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[firebase/agent-skills](https://github.com/firebase/agent-skills).
