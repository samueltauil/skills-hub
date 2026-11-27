# alloydb-basics

Manages clusters, instances, and backups for AlloyDB for PostgreSQL, and integrates with AlloyDB Model Context Protocol (MCP) tools for automated database operations. Use when creating, configuring, or administering AlloyDB databases. Do NOT use for general PostgreSQL instances (e.g. Cloud SQL) or other GCP databases.

This plugin packages the [`alloydb-basics`](skills/alloydb-basics/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/alloydb-basics) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/alloydb-basics/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install alloydb-basics@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dalloydb-basics),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `alloydb-basics`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
