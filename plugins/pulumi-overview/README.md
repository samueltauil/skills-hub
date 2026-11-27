# pulumi-overview

Use this skill for any task that creates, modifies, inspects, or destroys cloud infrastructure or SaaS configuration, from one-off CLI operations to full multi-resource projects, across providers in the Pulumi ecosystem. A typical project spans many providers (AWS or Azure or GCP, Kubernetes, Cloudflare, Auth0, Datadog, Vercel, and others), and Pulumi drives them through one CLI, one state model, and one credential layer. Trigger even when the user does not name Pulumi; phrasings like "deploy this app," "provision a database," "stand up a VPC," "configure Auth0," "set up Datadog monitoring," or "tear down staging" qualify. Also trigger for tasks that migrate, port, or convert existing infrastructure code (Terraform, CloudFormation, CDK, Bicep, ARM) to Pulumi. Do not trigger for application runtime code that reads or writes data via cloud SDKs; that is application code, not infrastructure.

This plugin packages the [`pulumi-overview`](skills/pulumi-overview/SKILL.md) skill from
[pulumi/agent-skills](https://github.com/pulumi/agent-skills/tree/main/pulumi/skills/pulumi-overview) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/pulumi-overview/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install pulumi-overview@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpulumi-overview),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `pulumi-overview`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[pulumi/agent-skills](https://github.com/pulumi/agent-skills).
