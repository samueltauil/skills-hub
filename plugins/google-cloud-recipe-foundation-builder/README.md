# google-cloud-recipe-foundation-builder

Deploys a baseline landing zone foundation for a Google Cloud Organization, establishing security guardrails using Organization Policies, resource hierarchy folders and projects, billing association, and centralized logging and monitoring. Deploys Google Cloud's recommended security controls and architecture. Use when setting up a new Google Cloud Organization or establishing a secure, enterprise-grade landing zone foundation. Don't use for individual project onboarding (use google-cloud-recipe-onboarding or product-specific skills instead).

This plugin packages the [`google-cloud-recipe-foundation-builder`](skills/google-cloud-recipe-foundation-builder/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/google-cloud-recipe-foundation-builder) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/google-cloud-recipe-foundation-builder/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install google-cloud-recipe-foundation-builder@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgoogle-cloud-recipe-foundation-builder),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `google-cloud-recipe-foundation-builder`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
