# azure-kubernetes

Plan, create, and configure production-ready Azure Kubernetes Service (AKS) clusters. Covers Day-0 checklist, SKU selection (Automatic vs Standard), networking options (private API server, Azure CNI Overlay, egress configuration), security, and operations (autoscaling, upgrade strategy, cost analysis). WHEN: create AKS environment, provision AKS, enable AKS observability, design AKS networking, choose AKS SKU, secure AKS, optimize AKS, AKS spot nodes, AKS cluster-autoscaler, rightsize AKS pod, pod rightsizing, over-provisioned AKS pod, pod resource requests and limits, Vertical Pod Autoscaler, VPA recommendations.

This plugin packages the [`azure-kubernetes`](skills/azure-kubernetes/SKILL.md) skill from
[microsoft/azure-skills](https://github.com/microsoft/azure-skills/tree/main/.github/plugins/azure-skills/skills/azure-kubernetes) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/azure-kubernetes/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install azure-kubernetes@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dazure-kubernetes),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `azure-kubernetes`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[microsoft/azure-skills](https://github.com/microsoft/azure-skills).
