# embedding-anisotropy-check

Use before reporting any cosine similarity computed over embeddings or transformer hidden states, whether the agent computed the vectors or loaded them. Measures the anisotropy of each side, centres by the population mean, and scores matched pairs against a permuted floor taken from the same comparison. Use when comparing one model's embeddings across precisions, runtimes or layers, when evaluating retrieval, probes or adapters, or before calling a similarity high, two conditions in agreement, or a small gap a null.

This plugin packages the [`embedding-anisotropy-check`](skills/embedding-anisotropy-check/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/embedding-anisotropy-check) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/embedding-anisotropy-check/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install embedding-anisotropy-check@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dembedding-anisotropy-check),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `embedding-anisotropy-check`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
