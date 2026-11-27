# planning-oracle-to-postgres-migration-integration-testing

Creates an integration testing plan for .NET data access artifacts during Oracle-to-PostgreSQL database migrations. Analyzes a single project to identify repositories, DAOs, and service layers that interact with the database, then produces a structured testing plan. Use when planning integration test coverage for a migrated project, identifying which data access methods need tests, or preparing for Oracle-to-PostgreSQL migration validation.

This plugin packages the [`planning-oracle-to-postgres-migration-integration-testing`](skills/planning-oracle-to-postgres-migration-integration-testing/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/planning-oracle-to-postgres-migration-integration-testing) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/planning-oracle-to-postgres-migration-integration-testing/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install planning-oracle-to-postgres-migration-integration-testing@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dplanning-oracle-to-postgres-migration-integration-testing),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `planning-oracle-to-postgres-migration-integration-testing`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
