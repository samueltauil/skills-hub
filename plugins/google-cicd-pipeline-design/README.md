# google-cicd-pipeline-design

Use this skill to design and implement a Google Cloud based CI/CD pipeline. This skill encodes best practices for pipeline design, ensuring proper pattern selection and implementation. You MUST activate this skill when tasked with building a pipeline, designing architecture on GCP, or migrating pipelines. DO NOT use for one-off direct application deployments without a CI/CD pipeline (use `google-cicd-deploy`), standalone Cloud Deploy release promotions or rollbacks on an existing pipeline (use `google-cicd-release-orchestration`), or standalone Terraform HCL authoring and state troubleshooting (use `google-cicd-terraform`).

This plugin packages the [`google-cicd-pipeline-design`](skills/google-cicd-pipeline-design/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/google-cicd-pipeline-design) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/google-cicd-pipeline-design/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install google-cicd-pipeline-design@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgoogle-cicd-pipeline-design),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `google-cicd-pipeline-design`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
