# gke-platform-security

Plans, configures, and hardens platform-level Google Kubernetes Engine (GKE) cluster security. Covers cluster add-ons (Secret Manager enablement), RBAC hardening (disabling insecure bindings, audit tools), Binary Authorization, Secrets Encryption (--database-encryption-key), Security Posture (--security-posture), enabling Shielded Nodes, GKE Sandbox cluster enablement, GKE IAM roles, and cross-service authentication IAM patterns. Use when securing cluster control planes, hardening GKE RBAC, enabling Shielded Nodes, enabling GKE Sandbox runtime, enabling cluster-wide security add-ons, or managing GKE IAM roles. Don't use for Workload Identity (use gke-workload-identity) or workload-level security (SecretProviderClass, PSS, NetPol, gVisor pod runtimeClassName; use gke-workload-security).

This plugin packages the [`gke-platform-security`](skills/gke-platform-security/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-platform-security) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-platform-security/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-platform-security@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-platform-security),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-platform-security`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
