# google-cicd-terraform

Architect, provision, and troubleshoot infrastructure on Google Cloud using Terraform. This skill ensures best practices like GCS backend usage and least-privilege IAM are followed. Enforces Google's Cloud Foundation Fabric patterns and rigorous validation protocols to ensure secure, idempotent, and scalable deployments across environments. Activate when the user requests infrastructure changes, pipeline design involving Terraform, or debugging Terraform issues. DO NOT use when deploying application code or container images directly via `gcloud` or `kubectl` without Terraform (use `google-cicd-deploy`), designing high-level CI/CD architecture before choosing an IaC tool (use `google-cicd-pipeline-design`), or managing Cloud Deploy releases and rollouts via `clouddeploy.yaml` (use `google-cicd-release-orchestration`).

This plugin packages the [`google-cicd-terraform`](skills/google-cicd-terraform/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/google-cicd-terraform) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/google-cicd-terraform/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install google-cicd-terraform@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgoogle-cicd-terraform),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `google-cicd-terraform`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
