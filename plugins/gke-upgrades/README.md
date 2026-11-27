# gke-upgrades

Plans, executes, and validates Google Kubernetes Engine (GKE) cluster upgrades and maintenance operations for both Standard and Autopilot clusters. Produces upgrade plans, pre/post-upgrade checklists, maintenance runbooks with gcloud commands, release channel strategy, and troubleshooting guides. Handles node pool upgrade strategies (surge, blue-green), version compatibility, PDB management, and workload-specific concerns (stateful, GPU, operators). Use this skill whenever the user mentions GKE upgrades, Kubernetes version bumps, node pool maintenance, GKE patching, cluster version management, release channel selection, maintenance windows, surge upgrades, stuck upgrades, or any GKE lifecycle management task — even casual mentions like "we need to upgrade our clusters" or "plan our next GKE maintenance" or "our upgrade is stuck." Don't use for GKE cluster creation, application onboarding, general networking/routing setup, or security policy configurations (use gke-basics or relevant GKE skills instead).

This plugin packages the [`gke-upgrades`](skills/gke-upgrades/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-upgrades) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-upgrades/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-upgrades@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-upgrades),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-upgrades`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
