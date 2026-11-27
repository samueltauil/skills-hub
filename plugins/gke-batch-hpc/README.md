# gke-batch-hpc

Runs batch and HPC workloads on GKE, utilizing job queues and parallel processing. Use when running GKE batch jobs, configuring GKE HPC, or setting up GKE job queues. Don't use for standard web application deployments (use gke-app-onboarding instead).

This plugin packages the [`gke-batch-hpc`](skills/gke-batch-hpc/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-batch-hpc) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-batch-hpc/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-batch-hpc@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-batch-hpc),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-batch-hpc`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
