# google-cicd-release-orchestration

Use this skill when you need to design Cloud Deploy delivery pipelines or manage releases for applications deploying to Cloud Run or Google Kubernetes Engine (GKE). This skill encodes best practices for multi-environment deployment, deployment strategies (like canary), and release management (including rollbacks and automations). Always activate this skill for these tasks to ensure robust and consistent configuration. DO NOT use for single-step direct deployments to Cloud Storage, Cloud Run, or GKE without Cloud Deploy (use `google-cicd-deploy`), end-to-end CI/CD source-to-build trigger architecture design (use `google-cicd-pipeline-design`), or Terraform HCL infrastructure provisioning (use `google-cicd-terraform`).

This plugin packages the [`google-cicd-release-orchestration`](skills/google-cicd-release-orchestration/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/google-cicd-release-orchestration) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/google-cicd-release-orchestration/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install google-cicd-release-orchestration@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgoogle-cicd-release-orchestration),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `google-cicd-release-orchestration`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
