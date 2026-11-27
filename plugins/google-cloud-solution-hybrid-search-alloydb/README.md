# google-cloud-solution-hybrid-search-alloydb

Discovers requirements and generates architectural, design, and deployment guidance for dynamic hybrid search systems by combining semantic search and keyword search. Optimized for AlloyDB hybrid search use cases in Google Cloud. Use when users need vector search combined with structured SQL filtering, faceted attributes, semantic reranking, in-database AI validation, or serverless hosting across transactional relational databases, analytical data warehouses, or managed database engines. DON'T use this skill for simple keyword-only search, or when a standalone non-relational vector database is required.

This plugin packages the [`google-cloud-solution-hybrid-search-alloydb`](skills/google-cloud-solution-hybrid-search-alloydb/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/google-cloud-solution-hybrid-search-alloydb) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/google-cloud-solution-hybrid-search-alloydb/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install google-cloud-solution-hybrid-search-alloydb@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgoogle-cloud-solution-hybrid-search-alloydb),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `google-cloud-solution-hybrid-search-alloydb`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
