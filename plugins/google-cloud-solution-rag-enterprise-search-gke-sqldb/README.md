# google-cloud-solution-rag-enterprise-search-gke-sqldb

Discovers requirements, and generates architectural, design, and deployment guidance for a retrieval-augmented generation (RAG)-capable enterprise search system in Google Cloud. Use when users need a vector-enabled SQL database as the store and index for the embedding vectors, an open model and open-source inferencing framework, and Kubernetes containers to host all the application components. DON'T use this skill for fully-managed RAG, or SaaS search services, or when a non-SQL vector database is required.

This plugin packages the [`google-cloud-solution-rag-enterprise-search-gke-sqldb`](skills/google-cloud-solution-rag-enterprise-search-gke-sqldb/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/google-cloud-solution-rag-enterprise-search-gke-sqldb) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/google-cloud-solution-rag-enterprise-search-gke-sqldb/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install google-cloud-solution-rag-enterprise-search-gke-sqldb@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgoogle-cloud-solution-rag-enterprise-search-gke-sqldb),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `google-cloud-solution-rag-enterprise-search-gke-sqldb`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
