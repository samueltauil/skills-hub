# provisioning

Provision and operate Elastic Cloud infrastructure: create, connect to, update, and delete Serverless projects (Elasticsearch, Observability, Security); manage traffic filters (IP and AWS PrivateLink network security); and manage the lifecycle of Elastic Cloud Hosted deployments. Use when creating or performing day-2 operations on serverless projects or hosted deployments, or restricting their network access.

This plugin packages the [`cloud-provisioning`](skills/cloud-provisioning/SKILL.md) skill from
[elastic/agent-skills](https://github.com/elastic/agent-skills/tree/main/skills/cloud/provisioning) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/provisioning/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install provisioning@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dprovisioning),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `provisioning`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[elastic/agent-skills](https://github.com/elastic/agent-skills).
