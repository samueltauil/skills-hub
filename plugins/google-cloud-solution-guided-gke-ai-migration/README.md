# google-cloud-solution-guided-gke-ai-migration

Guides the migration of existing AI workloads (Cloud Run, Gemini API, Gemini Enterprise Agent Platform) to self-hosted GKE inference using gcloud and kubectl. Use when the user has an existing AI inference workload (on Cloud Run, the Gemini API, Gemini Enterprise Agent Platform, or a custom VM) and wants to move it to self-hosted inference on GKE, or asks follow-up questions during such a migration (hardware sizing, model staging, manifest generation, validation, traffic cutover). DO NOT use for brand new GKE inference deployments with no existing workload to migrate (use gke-inference instead). DO NOT use if the user intends to automate the migration via the Gemini Cloud Assist MCP server.

This plugin packages the [`google-cloud-solution-guided-gke-ai-migration`](skills/google-cloud-solution-guided-gke-ai-migration/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/google-cloud-solution-guided-gke-ai-migration) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/google-cloud-solution-guided-gke-ai-migration/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install google-cloud-solution-guided-gke-ai-migration@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgoogle-cloud-solution-guided-gke-ai-migration),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `google-cloud-solution-guided-gke-ai-migration`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
