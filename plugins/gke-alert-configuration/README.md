# gke-alert-configuration

Configures alerting policies in Terraform for Google Kubernetes Engine (GKE) clusters, workloads, and services using PromQL and Google Cloud Managed Service for Prometheus. Use when writing, analyzing, validating, or deploying Terraform alerting policies to monitor GKE service latency, traffic, error rates using Multi-Window Multi-Burn-Rate SLO alerts, memory saturation, and cluster health such as CrashLoopBackOff and Node NotReady conditions. Don't use for non-GKE compute runtimes such as standalone Compute Engine VMs or standalone Cloud Run services without GKE.

This plugin packages the [`gke-alert-configuration`](skills/gke-alert-configuration/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-alert-configuration) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-alert-configuration/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-alert-configuration@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-alert-configuration),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-alert-configuration`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
