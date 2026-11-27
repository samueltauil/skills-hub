# huggingface-papers

Look up and read Hugging Face paper pages in markdown, and use the papers API for structured metadata such as authors, linked models/datasets/spaces, Github repo and project page. Use when the user shares a Hugging Face paper page URL, an arXiv URL or ID, or asks to summarize, explain, or analyze an AI research paper.

This plugin packages the [`huggingface-papers`](skills/huggingface-papers/SKILL.md) skill from
[huggingface/skills](https://github.com/huggingface/skills/tree/main/skills/huggingface-papers) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/huggingface-papers/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install huggingface-papers@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dhuggingface-papers),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `huggingface-papers`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[huggingface/skills](https://github.com/huggingface/skills).
