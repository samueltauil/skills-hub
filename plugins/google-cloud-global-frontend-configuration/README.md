# google-cloud-global-frontend-configuration

Guides agents through a 6-step discovery process to design and deploy Google Cloud global external Application Load Balancers with Cloud CDN, Cloud Armor, and Service Extensions, mapping workload requirements to best-practice configurations. Use when: - Designing, configuring, or deploying a Google Cloud global external Application Load Balancer, Cloud CDN, Cloud Armor WAF, or Service Extensions. - Discovering existing Google Cloud resources (Cloud Storage, MIGs, GKE, Cloud Run) to use as backends. - Generating production-grade Terraform HCL or gcloud CLI scripts for global external Application Load Balancers. - Actuating deployments via Infrastructure Manager or bash scripts, including IAM pre-checks. - Detecting, analyzing, or reconciling configuration drift on deployed global external Application Load Balancers. Don't use for: - Non-Google Cloud load balancing or security configurations. - Purely regional or internal load balancing setups (unless part of a hybrid/failover global design).

This plugin packages the [`google-cloud-global-frontend-configuration`](skills/google-cloud-global-frontend-configuration/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/google-cloud-global-frontend-configuration) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/google-cloud-global-frontend-configuration/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install google-cloud-global-frontend-configuration@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgoogle-cloud-global-frontend-configuration),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `google-cloud-global-frontend-configuration`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
