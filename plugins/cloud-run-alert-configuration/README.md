# cloud-run-alert-configuration

Configures best-practice, high-signal alerting policies for Cloud Run resources on Google Cloud (services, jobs, and worker pools) based on seasoned SRE practices. Use when analyzing, recommending, writing, or deploying Terraform PromQL alerting policies to monitor Cloud Run error rates (4xx/5xx), request latency, container instance saturation (warning/critical), container CPU/memory utilization and allocation, billable instance time, job execution status, and worker pool queue backlog. Don't use for GKE workloads (use gke-alert-configuration) or Compute Engine VMs.

This plugin packages the [`cloud-run-alert-configuration`](skills/cloud-run-alert-configuration/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/cloud-run-alert-configuration) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/cloud-run-alert-configuration/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install cloud-run-alert-configuration@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcloud-run-alert-configuration),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `cloud-run-alert-configuration`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
