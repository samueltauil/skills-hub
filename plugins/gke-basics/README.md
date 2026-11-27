# gke-basics

Manages core GKE cluster provisioning, credentials, Autopilot vs Standard selection, and workload deployment. Use when creating GKE clusters, fetching kubectl credentials, or deciding between Autopilot and Standard modes. Don't use for Workload Identity (use gke-workload-identity), GKE networking (use gke-networking), security hardening (use gke-platform-security or gke-workload-security), or cluster upgrades (use gke-upgrades).

This plugin packages the [`gke-basics`](skills/gke-basics/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-basics) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-basics/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-basics@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-basics),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-basics`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
