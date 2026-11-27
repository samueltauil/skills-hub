# compute-host-events-troubleshooting

Investigates, diagnoses, and mitigates Google Compute Engine virtual machine (VM) host events, including planned infrastructure maintenance (migrateOnHostMaintenance, terminateOnHostMaintenance), physical host hardware errors (hostError), guest OS terminations (guestTerminate), and Spot or Preemptible VM preemptions (compute.instances.preempted) using shutdown-script metadata. Use ONLY when an existing Compute Engine VM unexpectedly reboots, stops, crashes, is preempted, or becomes unresponsive due to physical host maintenance, hardware errors, or Local SSD recovery. DO NOT read or use for creating new standalone VMs, Managed Instance Group (MIG) autoscaler scale-out or scale-in failures, Google Kubernetes Engine (GKE) clusters, application OOM debugging, or VPC firewall issues.

This plugin packages the [`compute-host-events-troubleshooting`](skills/compute-host-events-troubleshooting/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/compute-host-events-troubleshooting) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/compute-host-events-troubleshooting/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install compute-host-events-troubleshooting@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcompute-host-events-troubleshooting),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `compute-host-events-troubleshooting`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
