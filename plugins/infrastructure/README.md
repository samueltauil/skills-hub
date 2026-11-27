# infrastructure

Ship Kubernetes, host, container, and cloud-provider telemetry into Grafana Cloud — `k8s-monitoring` Helm chart for K8s clusters (metrics + logs + traces + events + cost), Alloy `prometheus.exporter.unix` for Linux hosts, cAdvisor + Docker discovery for containers, and CloudWatch / Azure Monitor / Google Cloud Monitoring datasource setup. Use when onboarding a new cluster or VM fleet to Grafana Cloud, picking the right Helm values for K8s scraping, wiring kube-state-metrics + node-exporter + cAdvisor, alerting on `PodCrashLooping` / node memory / PVC capacity, or pulling AWS / Azure / GCP cloud metrics — even when the user says "monitor my cluster", "send K8s metrics to Grafana", "scrape EC2 metrics", "cluster pod logs", or "install the monitoring helm chart" without naming `k8s-monitoring` or Alloy.

This plugin packages the [`infrastructure`](skills/infrastructure/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-cloud/infrastructure) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/infrastructure/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install infrastructure@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dinfrastructure),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `infrastructure`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
