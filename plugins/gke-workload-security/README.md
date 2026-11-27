# gke-workload-security

Audits, configures, and hardens workload-level security controls for Google Kubernetes Engine (GKE) applications and namespaces. Covers running security audits (`audit_cluster.sh`), enforcing Network Policies (default-deny and Dataplane V2 logging), isolating high-risk pods inside GKE Sandbox (`gVisor`), enforcing Pod Security Standards (`restricted` labeling) and pod securityContext, and mounting Secret Manager secrets via CSI (`SecretProviderClass`). Use when auditing workload security posture, isolating namespaces, applying pod security standards, or configuring network policies and secret volume mounts. Don't use for Workload Identity (use gke-workload-identity), cluster-wide control plane security, RBAC hardening, Binary Authorization, Shielded Nodes, or enabling platform-level GKE add-ons (use gke-platform-security instead).

This plugin packages the [`gke-workload-security`](skills/gke-workload-security/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-workload-security) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-workload-security/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-workload-security@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-workload-security),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-workload-security`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
