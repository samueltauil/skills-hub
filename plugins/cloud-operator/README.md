# cloud-operator

Google Cloud (GCP) assistant and operator via the `autocloud` MCP server. Use for any GCP request: how-to, resources, Terraform/Kubernetes/Helm, rollouts, incidents, costs. Invoke it before answering a GCP question from your own knowledge or documentation search, and before proposing an architecture or backend, even when no cloud is named. Invoke it before reading or editing local *.tf or Kubernetes YAML. Don't use for non-GCP tasks or local machine setup like installing gcloud and setting up GCP.

This plugin packages the [`cloud-operator`](skills/cloud-operator/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/cloud-operator) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/cloud-operator/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install cloud-operator@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcloud-operator),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `cloud-operator`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
