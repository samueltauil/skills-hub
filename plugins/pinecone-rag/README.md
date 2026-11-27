# pinecone-rag

Build production RAG pipelines and persistent agent memory using Pinecone as the vector database backend. ALWAYS USE THIS SKILL when the user mentions Pinecone, wants to index documents for semantic search, build a retrieval-augmented generation system, store agent memory across sessions, implement hybrid search, or connect an LLM to a searchable knowledge base — even if they don't say "Pinecone" explicitly. Also use when the user asks about vector databases for RAG, namespace isolation for multi-tenant agents, embedding pipelines, or scaling a knowledge base beyond what local storage can handle. DO NOT use for local-only vector stores (Chroma, FAISS, pgvector) or pure keyword search with no semantic component.

This plugin packages the [`pinecone-rag`](skills/pinecone-rag/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/pinecone-rag) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/pinecone-rag/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install pinecone-rag@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpinecone-rag),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `pinecone-rag`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
