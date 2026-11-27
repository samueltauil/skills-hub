# gke-ai-troubleshooting-jobset-interruption

Diagnoses GKE JobSet interruptions, restarts, and preemptions for AI/ML training workloads autonomously. Use when troubleshooting JobSet restart loops, spot VM preemptions, node readiness failures, host VM issues, or coordinator worker crashes. Don't use for general GKE cluster creation, basic workload deployment, or non-JobSet application issues.

This plugin packages the [`gke-ai-troubleshooting-jobset-interruption`](skills/gke-ai-troubleshooting-jobset-interruption/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-ai-troubleshooting-jobset-interruption) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-ai-troubleshooting-jobset-interruption/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-ai-troubleshooting-jobset-interruption@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-ai-troubleshooting-jobset-interruption),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-ai-troubleshooting-jobset-interruption`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
