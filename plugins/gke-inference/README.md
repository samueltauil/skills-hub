# gke-inference

Deploys and optimizes AI/ML inference workloads on GKE, using GPUs, TPUs, and model servers. Use when deploying GKE inference servers, configuring GKE GPU resources for inference, or deploying LLMs on GKE. Don't use for migrating existing AI workloads to GKE (use google-cloud-solution-guided-gke-ai-migration), GKE RAG with Cloud SQL/AlloyDB (use google-cloud-solution-rag-enterprise-search-gke-sqldb), or batch/HPC (use gke-batch-hpc).

This plugin packages the [`gke-inference`](skills/gke-inference/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-inference) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-inference/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-inference@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-inference),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-inference`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
