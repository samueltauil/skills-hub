# creating-oracle-to-postgres-migration-integration-tests

Creates integration test cases targeting Oracle for .NET data access artifacts. Tests capture Oracle expected behavior as the authoritative baseline; they are written once and later ported to PostgreSQL by migrating the test project in Phase 6. Use only during Phase 3, before any PostgreSQL migration work has begun. Do not invoke during Phase 6 or against a project that has already been migrated.

This plugin packages the [`creating-oracle-to-postgres-migration-integration-tests`](skills/creating-oracle-to-postgres-migration-integration-tests/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/creating-oracle-to-postgres-migration-integration-tests) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/creating-oracle-to-postgres-migration-integration-tests/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install creating-oracle-to-postgres-migration-integration-tests@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcreating-oracle-to-postgres-migration-integration-tests),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `creating-oracle-to-postgres-migration-integration-tests`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
