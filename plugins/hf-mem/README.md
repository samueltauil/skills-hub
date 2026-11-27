# hf-mem

Estimate the GPU memory needed to run a Hugging Face model (weights, KV cache and inference overhead) and whether it fits on given GPUs, without downloading it. Use when asked how much VRAM a model needs, whether it fits on a GPU, the longest context that fits, or which GGUF quantization to pick.

This plugin packages the [`hf-mem`](skills/hf-mem/SKILL.md) skill from
[huggingface/skills](https://github.com/huggingface/skills/tree/main/skills/hf-mem) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/hf-mem/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install hf-mem@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dhf-mem),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `hf-mem`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[huggingface/skills](https://github.com/huggingface/skills).
