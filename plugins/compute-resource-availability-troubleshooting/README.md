# compute-resource-availability-troubleshooting

Diagnoses, mitigates, and prevents Google Compute Engine resource availability and capacity stockout errors (ZONE_RESOURCE_POOL_EXHAUSTED, ZONE_RESOURCE_POOL_EXHAUSTED_WITH_DETAILS, and machine type or accelerator unavailable in zone). Use ONLY when VM creation, Managed Instance Group (MIG) scale-out, or stopped instance startup fails due to regional or zonal hardware capacity exhaustion for GPUs, TPUs, or specific CPU shapes. DO NOT read or use for IAM permission errors, project quota limit increases without stockouts, general greenfield VM creation, or unexpected host reboots on already-running VMs.

This plugin packages the [`compute-resource-availability-troubleshooting`](skills/compute-resource-availability-troubleshooting/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/compute-resource-availability-troubleshooting) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/compute-resource-availability-troubleshooting/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install compute-resource-availability-troubleshooting@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcompute-resource-availability-troubleshooting),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `compute-resource-availability-troubleshooting`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
