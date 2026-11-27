# reviewing-oracle-to-postgres-migration

Identifies Oracle-to-PostgreSQL migration risks by cross-referencing code against known behavioral differences (empty strings, refcursors, type coercion, sorting/collations, UNION ALL planner risks, materialized-view refresh requirements, timestamps, concurrent transactions, etc.). Use when planning a database migration, reviewing migration artifacts, or validating that integration tests cover Oracle/PostgreSQL differences.

This plugin packages the [`reviewing-oracle-to-postgres-migration`](skills/reviewing-oracle-to-postgres-migration/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/reviewing-oracle-to-postgres-migration) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/reviewing-oracle-to-postgres-migration/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install reviewing-oracle-to-postgres-migration@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dreviewing-oracle-to-postgres-migration),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `reviewing-oracle-to-postgres-migration`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
