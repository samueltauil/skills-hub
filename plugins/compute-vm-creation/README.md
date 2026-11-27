# compute-vm-creation

Guides the planning, configuration, and provisioning of standalone Google Compute Engine virtual machines (VMs) and bare metal (-metal) instances using gcloud CLI commands or direct MCP tool execution. Use ONLY when the user wants to create, configure, or provision a new standalone Compute Engine VM or bare metal instance from conversational intents (hardware sizing, region selection, OS image, networking, security defaults). DO NOT read or use for Google Kubernetes Engine (GKE) Autopilot or Standard clusters, Kubernetes node pools or Pods, container orchestration, managing existing VMs, Managed Instance Groups (MIGs), or Instance Templates.

This plugin packages the [`compute-vm-creation`](skills/compute-vm-creation/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/compute-vm-creation) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/compute-vm-creation/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install compute-vm-creation@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcompute-vm-creation),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `compute-vm-creation`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
