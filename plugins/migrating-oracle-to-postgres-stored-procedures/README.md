# migrating-oracle-to-postgres-stored-procedures

Migrates Oracle PL/SQL stored procedures to PostgreSQL PL/pgSQL. Translates Oracle-specific syntax, preserves method signatures and type-anchored parameters, leverages orafce where appropriate, and applies explicit collation mapping (`COLLATE "C"` only when appropriate, locale collations when required). Use when converting Oracle stored procedures or functions to PostgreSQL equivalents during a database migration.

This plugin packages the [`migrating-oracle-to-postgres-stored-procedures`](skills/migrating-oracle-to-postgres-stored-procedures/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/migrating-oracle-to-postgres-stored-procedures) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/migrating-oracle-to-postgres-stored-procedures/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install migrating-oracle-to-postgres-stored-procedures@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmigrating-oracle-to-postgres-stored-procedures),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `migrating-oracle-to-postgres-stored-procedures`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
