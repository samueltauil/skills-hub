# gke-workload-identity

Configures and diagnoses Workload Identity Federation for GKE authentication failures for Pods (403 "iam.serviceAccounts.getAccessToken" / permission denied, "could not find default credentials", or GKE metadata server unreachable) by verifying cluster and node-pool Workload Identity configuration, the Kubernetes ServiceAccount (KSA) to IAM binding (direct principal binding and legacy Google ServiceAccount impersonation), target-resource IAM roles, and gke-metadata-server health. Use when setting up KSA/GSA bindings (`roles/iam.workloadIdentityUser`, `iam.gke.io/gcp-service-account`) or when a Pod cannot authenticate to Google Cloud APIs. Don't use for in-cluster Kubernetes RBAC errors (API-server authorization), general workload crashes (use gke-workload-troubleshooting), or Pod Security Standards and NetworkPolicies (use gke-workload-security).

This plugin packages the [`gke-workload-identity`](skills/gke-workload-identity/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-workload-identity) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-workload-identity/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-workload-identity@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-workload-identity),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-workload-identity`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
