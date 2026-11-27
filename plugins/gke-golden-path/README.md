# gke-golden-path

Provides GKE golden path configuration defaults, production readiness checklists, and cluster default patterns. Use when designing GKE clusters, verifying GKE production readiness, or checking configurations against GKE defaults. Don't use for setting up workload autoscaling specifically (use gke-workload-scaling instead).

This plugin packages the [`gke-golden-path`](skills/gke-golden-path/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-golden-path) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-golden-path/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-golden-path@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-golden-path),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-golden-path`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
