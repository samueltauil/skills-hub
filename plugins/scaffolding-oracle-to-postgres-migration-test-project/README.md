# scaffolding-oracle-to-postgres-migration-test-project

Scaffolds an xUnit integration test project targeting Oracle in .NET solutions. Creates the test project, transaction-rollback base class, and seed data manager. Use only during Phase 3, before writing Oracle baseline integration tests. Do not invoke during Phase 6 — the PostgreSQL test project is produced by migrating this project, not by running this skill again.

This plugin packages the [`scaffolding-oracle-to-postgres-migration-test-project`](skills/scaffolding-oracle-to-postgres-migration-test-project/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/scaffolding-oracle-to-postgres-migration-test-project) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/scaffolding-oracle-to-postgres-migration-test-project/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install scaffolding-oracle-to-postgres-migration-test-project@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dscaffolding-oracle-to-postgres-migration-test-project),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `scaffolding-oracle-to-postgres-migration-test-project`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
