# gke-workload-troubleshooting

Diagnoses GKE workload failures (CrashLoopBackOff, OOMKilled, ImagePullBackOff, Pending, etc.) via logs and events. Use when pods fail to start or crash repeatedly. Don't use for GKE cluster infrastructure provisioning, node pool creation, or non-Kubernetes Google Cloud services.

This plugin packages the [`gke-workload-troubleshooting`](skills/gke-workload-troubleshooting/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-workload-troubleshooting) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-workload-troubleshooting/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-workload-troubleshooting@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-workload-troubleshooting),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-workload-troubleshooting`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
