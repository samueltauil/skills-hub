# gke-observability

Configures GKE observability, including Cloud Logging, Cloud Monitoring, and managed Prometheus. Use when configuring GKE monitoring, setting up GKE logging, or configuring Prometheus metrics collection, to diagnose GKE control plane, API server, admission webhook, etcd storage, node registration or label, and pod eviction, preemption, or scheduling issues using GKE metrics, Kubernetes events, and Cloud Logging, and to troubleshoot Managed Service for Prometheus (GMP) issues such as missing metrics, unhealthy scrape targets, PodMonitoring misconfiguration, rule/alert evaluation failures, and monitoring permission errors. Don't use to configure local application logging frameworks or external APMs outside GKE.

This plugin packages the [`gke-observability`](skills/gke-observability/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-observability) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-observability/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-observability@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-observability),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-observability`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
