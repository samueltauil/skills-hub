# firebase-analytics

Comprehensive guide for Google Analytics for Firebase (GA4F), including base setup, SDK initialization, screen tracking, and event logging on Android and iOS. Use this skill when setting up Google Analytics, adding the SDK, or logging analytics events. Don't use for standalone CLI login or project/config file downloads without Analytics (use firebase-basics), or for Crashlytics, Remote Config, Auth, Firestore, Hosting, App Hosting, or Data Connect.

This plugin packages the [`firebase-analytics`](skills/firebase-analytics/SKILL.md) skill from
[firebase/agent-skills](https://github.com/firebase/agent-skills/tree/main/skills/firebase-analytics) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/firebase-analytics/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install firebase-analytics@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dfirebase-analytics),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `firebase-analytics`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[firebase/agent-skills](https://github.com/firebase/agent-skills).
