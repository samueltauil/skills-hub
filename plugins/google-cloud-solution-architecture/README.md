# google-cloud-solution-architecture

Interactively discovers requirements and designs holistic, multi-product system architectures, solution blueprints, and deployment recommendations for complex workloads on Google Cloud. Use when designing end-to-end cloud solutions, selecting and integrating Google Cloud services, generating architecture diagrams, or conducting requirements discovery for new cloud workloads or migrations. Don't use for single-product tasks (use product-specific skills), initial onboarding or authentication (use google-cloud-recipe-*), Well-Architected Framework reviews or audits (use google-cloud-waf-*), or workloads covered by specialized solution skills.

This plugin packages the [`google-cloud-solution-architecture`](skills/google-cloud-solution-architecture/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/google-cloud-solution-architecture) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/google-cloud-solution-architecture/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install google-cloud-solution-architecture@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgoogle-cloud-solution-architecture),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `google-cloud-solution-architecture`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
