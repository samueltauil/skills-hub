# gke-service-networking

Configures GKE edge networking, traffic routing, load balancing, and private service endpoints. Use when configuring Gateway API manifests, standard Ingress, Cloud Armor WAF security policies, Container-Native Load Balancing (NEGs), Private Service Connect (PSC), or Google-managed SSL certificates on GKE, and to troubleshoot Ingress and load-balancer 502/5xx errors, backend health-check failures, connection draining, and TLS/SSL policy enforcement. Don't use for core cluster IP planning, Dataplane V2 network policies, or node NAT egress (use gke-networking instead).

This plugin packages the [`gke-service-networking`](skills/gke-service-networking/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-service-networking) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-service-networking/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-service-networking@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-service-networking),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-service-networking`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
