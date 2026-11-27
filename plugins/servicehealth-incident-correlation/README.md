# servicehealth-incident-correlation

Checks Personalized Service Health (PSH) events and resource-level impacts to determine whether a Google Cloud incident affects a project or its resources, returning an impact verdict with affected resources, published symptoms, and workarounds. Use when asked whether Google Cloud is having an outage or affecting a project or its resources, when looking up a PSH event, or when triaging live Google Cloud workload issues or alerts whose symptoms suggest a possible Google Cloud service disruption—even if the user does not suspect an outage. Don't use for local code or build errors, routine alerts or automations that neither ask for a service health check nor suggest a platform disruption, configuring PSH alerts, or checking non-project-specific public status.

This plugin packages the [`servicehealth-incident-correlation`](skills/servicehealth-incident-correlation/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/servicehealth-incident-correlation) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/servicehealth-incident-correlation/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install servicehealth-incident-correlation@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dservicehealth-incident-correlation),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `servicehealth-incident-correlation`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
