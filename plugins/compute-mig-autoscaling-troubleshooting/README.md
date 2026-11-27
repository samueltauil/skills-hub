# compute-mig-autoscaling-troubleshooting

Diagnoses and resolves Google Compute Engine Managed Instance Group (MIG) autoscaling failures, scale-out blocks, and scale-in stalls. Use ONLY when a Compute Engine MIG fails to add or remove VM instances during load changes, hits quota or zonal stockout limits, reaches maxNumReplicas (CAPPED_AT_MAX_NUM_REPLICAS), conflicts with HTTP(S) load balancer maxRate settings, fails to scale in to zero instances, or fails to read Cloud Monitoring scaling metrics. DO NOT read or use for Google Kubernetes Engine (GKE) Horizontal Pod Autoscaler (HPA), GKE Cluster Autoscaler, standalone single-VM creation, or single-VM host maintenance reboots.

This plugin packages the [`compute-mig-autoscaling-troubleshooting`](skills/compute-mig-autoscaling-troubleshooting/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/compute-mig-autoscaling-troubleshooting) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/compute-mig-autoscaling-troubleshooting/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install compute-mig-autoscaling-troubleshooting@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcompute-mig-autoscaling-troubleshooting),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `compute-mig-autoscaling-troubleshooting`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
