# gke-cluster-creation

Plans and executes GKE cluster creation, provisioning, and production readiness audits using pre-defined templates (Autopilot, Standard Regional, GPU/AI Inference, AI Hypercompute). Use when creating GKE clusters, provisioning GKE environments, selecting cluster modes, or auditing GKE clusters. Don't use for application onboarding or deployment configuration (use gke-app-onboarding instead).

This plugin packages the [`gke-cluster-creation`](skills/gke-cluster-creation/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-cluster-creation) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-cluster-creation/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-cluster-creation@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-cluster-creation),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-cluster-creation`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
