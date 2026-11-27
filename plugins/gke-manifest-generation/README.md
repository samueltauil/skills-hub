# gke-manifest-generation

Generates and updates secure, production-ready Kubernetes YAML manifests optimized for GKE Autopilot and GKE Standard clusters. Use when creating or modifying GKE deployment manifests, configuring container security contexts, setting CPU/memory resource limits, defining readiness/liveness/startup probes, mounting secrets and volumes, configuring GKE Gateway API routes, targeting Spot VMs, or deploying AI model inference workloads (vLLM, TGI, Gemma). Don't use for live cluster operations, pod troubleshooting (use gke-workload-troubleshooting), or cluster infrastructure provisioning (use gke-cluster-creation).

This plugin packages the [`gke-manifest-generation`](skills/gke-manifest-generation/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-manifest-generation) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-manifest-generation/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-manifest-generation@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-manifest-generation),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-manifest-generation`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
