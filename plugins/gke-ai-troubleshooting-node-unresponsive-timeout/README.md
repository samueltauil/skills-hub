# gke-ai-troubleshooting-node-unresponsive-timeout

Diagnose and mitigate GKE TPU or GPU nodes stuck in NotReady / NodeStatusUnknown ("Kubelet stopped posting node status") due to host kernel panics, hardware lockups, or disabled node auto-repair. Use when nodes stop heartbeating beyond the node auto-repair threshold and pods remain stuck in Terminating. Don't use for healthy nodes, pod-only application crashes, or routine GKE upgrades.

This plugin packages the [`gke-ai-troubleshooting-node-unresponsive-timeout`](skills/gke-ai-troubleshooting-node-unresponsive-timeout/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-ai-troubleshooting-node-unresponsive-timeout) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-ai-troubleshooting-node-unresponsive-timeout/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-ai-troubleshooting-node-unresponsive-timeout@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-ai-troubleshooting-node-unresponsive-timeout),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-ai-troubleshooting-node-unresponsive-timeout`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
