# gke-productionize

Orchestrates comprehensive production readiness reviews and assessments for GKE clusters and workloads across scalability, security, reliability, observability, backup/DR, and cost optimization. Use when asked to productionize, prepare, assess, audit, or review a GKE cluster or workload before going live to production. Don't use for deep-dive single-domain implementation (use specific domain skills like gke-workload-scaling, gke-platform-security, gke-workload-security, gke-service-networking, gke-reliability instead).

This plugin packages the [`gke-productionize`](skills/gke-productionize/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-productionize) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-productionize/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-productionize@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-productionize),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-productionize`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
