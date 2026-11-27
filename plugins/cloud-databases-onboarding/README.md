# cloud-databases-onboarding

Guides users through discovering their database requirements, recommends a Google Cloud database based on a recommendation matrix, and assists in database creation. Use when a user asks 'What database service should I use?', 'Help me pick a database', or when a user wants to create a new database on Google Cloud. Don't use for general Google Cloud maintenance, managing existing databases, or database migrations.

This plugin packages the [`cloud-databases-onboarding`](skills/cloud-databases-onboarding/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/cloud-databases-onboarding) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/cloud-databases-onboarding/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install cloud-databases-onboarding@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcloud-databases-onboarding),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `cloud-databases-onboarding`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
