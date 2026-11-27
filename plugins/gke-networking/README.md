# gke-networking

Plans, configures, and manages core GKE cluster networking. Covers private clusters, VPC-native configurations, DNS, node egress, Dataplane V2, and IP planning. Use when designing GKE networking layouts, configuring private clusters, setting up Dataplane V2, planning GKE IP ranges, or managing VPC- native cluster modes. Don't use for application ingress, load balancing, or service networking (use gke-service-networking instead).

This plugin packages the [`gke-networking`](skills/gke-networking/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-networking) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-networking/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-networking@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-networking),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-networking`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
