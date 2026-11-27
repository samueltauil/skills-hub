# spanner-graph-query-tuning

Tunes and troubleshoots Spanner Graph on Google Cloud ISO GQL queries and execution plans. Use when optimizing slow Spanner Graph GQL queries, diagnosing distributed cross apply versus hash join execution operators and index seek prefixes, eliminating multi-arm star query Cartesian products with chained query aggregation, bounding super-node fan-out, decorrelating slow subqueries or optional matches, optimizing deep quantified variable-length paths, or applying join method, index, and path factorization query hints. Don't use for relational-to-property-graph schema mapping over existing relational tables (use spanner-relational-to-graph) or physical schema, table, and interleaving design (use spanner-graph-schema-best-practices).

This plugin packages the [`spanner-graph-query-tuning`](skills/spanner-graph-query-tuning/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/spanner-graph-query-tuning) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/spanner-graph-query-tuning/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install spanner-graph-query-tuning@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dspanner-graph-query-tuning),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `spanner-graph-query-tuning`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
