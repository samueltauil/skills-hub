# huggingface-best

Use when the user asks about finding the best, top, or recommended model for a task, wants to know what AI model to use, or wants to compare models by benchmark scores. Triggers on: "best model for X", "what model should I use for", "top models for [task]", "which model runs on my laptop/machine/device", "recommend a model for", "what LLM should I use for", "compare models for", "what's state of the art for", or any question about choosing an AI model for a specific use case. Always use this skill when the user wants model recommendations or comparisons, even if they don't explicitly mention HuggingFace or benchmarks.

This plugin packages the [`huggingface-best`](skills/huggingface-best/SKILL.md) skill from
[huggingface/skills](https://github.com/huggingface/skills/tree/main/skills/huggingface-best) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/huggingface-best/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install huggingface-best@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dhuggingface-best),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `huggingface-best`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[huggingface/skills](https://github.com/huggingface/skills).
