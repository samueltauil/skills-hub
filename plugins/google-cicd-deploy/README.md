# google-cicd-deploy

Use this skill when requested to deploy an application to Google Cloud (GCS, Cloud Run, GKE) or when analyzing an application to determine the best deployment target. **Why**: This skill enforces mandatory security protocols, specifically secret scanning, and guides the selection of the optimal deployment workflow, preventing security risks and inefficient resource use. Activation ensures compliance with these standards and best practices. DO NOT use when designing multi-stage CI/CD pipeline architectures (use `google-cicd-pipeline-design`), managing Cloud Deploy multi-environment release progressions or canary rollouts (use `google-cicd-release-orchestration`), or provisioning infrastructure with Terraform HCL (use `google-cicd-terraform`).

This plugin packages the [`google-cicd-deploy`](skills/google-cicd-deploy/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/google-cicd-deploy) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/google-cicd-deploy/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install google-cicd-deploy@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgoogle-cicd-deploy),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `google-cicd-deploy`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
