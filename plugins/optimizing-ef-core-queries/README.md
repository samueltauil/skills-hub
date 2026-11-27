# optimizing-ef-core-queries

Review and optimize application data access that uses Entity Framework Core (EF Core). Use for EF Core performance and correctness reviews of services, repositories, imports, and background jobs: slow or memory-heavy queries, excessive round-trips, hidden SaveChanges, premature materialization, dynamic query construction, result-graph tracking, bulk writes, DbContext lifetime or overlapping operations, search semantics, paging, raw SQL, and model/index coverage. Use whether or not EF Core owns the schema. For EF Core, not Dapper or raw ADO.NET.

This plugin packages the [`optimizing-ef-core-queries`](skills/optimizing-ef-core-queries/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-data/skills/optimizing-ef-core-queries) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/optimizing-ef-core-queries/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install optimizing-ef-core-queries@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Doptimizing-ef-core-queries),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `optimizing-ef-core-queries`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
