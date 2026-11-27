# migrating-oracle-to-postgres-data-access-code

Migrates .NET/C# data access code from Oracle to PostgreSQL (Npgsql). Replaces Oracle NuGet packages, rewrites OracleConnection/OracleCommand/OracleDataReader usage, fixes DbType mappings, updates stored procedure invocation patterns, and adapts connection string configuration. Use when migrating the application code layer of a .NET project during an Oracle-to-PostgreSQL database migration.

This plugin packages the [`migrating-oracle-to-postgres-data-access-code`](skills/migrating-oracle-to-postgres-data-access-code/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/migrating-oracle-to-postgres-data-access-code) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/migrating-oracle-to-postgres-data-access-code/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install migrating-oracle-to-postgres-data-access-code@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmigrating-oracle-to-postgres-data-access-code),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `migrating-oracle-to-postgres-data-access-code`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
