# gke-app-onboarding

Manages GKE application onboarding, covering containerization, deployment manifests, and migration. Use when onboarding or deploying an application to GKE for the first time, or containerizing an app for GKE. Don't use for general GKE cluster administration or upgrades (use gke-basics or gke-upgrades instead).

This plugin packages the [`gke-app-onboarding`](skills/gke-app-onboarding/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-app-onboarding) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-app-onboarding/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-app-onboarding@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-app-onboarding),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-app-onboarding`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
