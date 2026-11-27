# train-sentence-transformers

Train or fine-tune sentence-transformers models across `SentenceTransformer` (bi-encoder, dense or static embedding model for retrieval, similarity, clustering, classification, paraphrase mining, dedup, multimodal), `CrossEncoder` (reranker, pair scoring for two-stage retrieval / pair classification), `SparseEncoder` (SPLADE, sparse embedding model for learned-sparse retrieval), and `MultiVectorEncoder` (ColBERT / late-interaction, per-token embeddings scored with MaxSim). Covers loss selection, hard-negative mining, evaluators, distillation, LoRA, Matryoshka, and Hugging Face Hub publishing. Use for any sentence-transformers training task.

This plugin packages the [`train-sentence-transformers`](skills/train-sentence-transformers/SKILL.md) skill from
[huggingface/skills](https://github.com/huggingface/skills/tree/main/skills/train-sentence-transformers) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/train-sentence-transformers/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install train-sentence-transformers@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dtrain-sentence-transformers),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `train-sentence-transformers`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[huggingface/skills](https://github.com/huggingface/skills).
