# application-design-center-design-deploy

Processes GCP infrastructure design and deployment workflows within Application Design Center (ADC). Use when: - Designing GCP infrastructure with Terraform. - Validating local HCL. - Performing best-practice plan scans. - Importing templates to Application Design Center (ADC). - Deploying templates. - Troubleshooting deployment failures. Boundaries: - Only use for GCP-specific cloud infrastructure. - Only use for Terraform coding within the ADC context.

This plugin packages the [`application-design-center-design-deploy`](skills/application-design-center-design-deploy/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/application-design-center-design-deploy) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/application-design-center-design-deploy/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install application-design-center-design-deploy@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dapplication-design-center-design-deploy),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `application-design-center-design-deploy`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
