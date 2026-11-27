# gke-multitenancy

Plans and configures multi-tenancy on GKE. Covers namespace isolation, RBAC planning for teams, resource quotas, LimitRanges, network isolation, and cost allocation. Use when designing GKE multi-tenancy, configuring GKE namespaces, setting up resource quotas, or isolating GKE teams. Don't use for single-tenant cluster configuration or general deployment instructions (use gke-basics or gke-app-onboarding instead).

This plugin packages the [`gke-multitenancy`](skills/gke-multitenancy/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-multitenancy) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-multitenancy/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-multitenancy@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-multitenancy),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-multitenancy`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
