# google-cloud-waf-cost-optimization

Evaluates Google Cloud workloads for cost efficiency and FinOps alignment using the Google Cloud Well-Architected Framework Cost Optimization pillar. Use when the user asks to analyze Google Cloud spend, reduce cloud bills, rightsize resources (for example, Compute, GKE, Storage, Databases), evaluate discount options (for example, CUDs, SUDs, Spot VMs), or eliminate idle capacity. Do not use for standalone product pricing lookups or non-cost architecture design.

This plugin packages the [`google-cloud-waf-cost-optimization`](skills/google-cloud-waf-cost-optimization/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/google-cloud-waf-cost-optimization) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/google-cloud-waf-cost-optimization/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install google-cloud-waf-cost-optimization@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgoogle-cloud-waf-cost-optimization),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `google-cloud-waf-cost-optimization`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
