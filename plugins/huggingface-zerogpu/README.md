# huggingface-zerogpu

AI demos and GPU compute with Gradio Spaces and Hugging Face Spaces ZeroGPU. Use when writing or reviewing code that uses `@spaces.GPU`, configuring `python_version` or `requirements.txt` for a ZeroGPU Space, or handling ZeroGPU-specific code constraints — pickle-based process isolation, `gr.State` semantics across the worker boundary, no `torch.compile` (use AoTI instead), CUDA wheel-only builds (no `nvcc` at build or runtime), large vs xlarge sizing, and dynamic duration callables. Make sure to use this skill whenever the user mentions ZeroGPU, `@spaces.GPU`, or the `spaces` Python package, or hits ZeroGPU-specific code errors like `PicklingError` across the worker boundary, `illegal duration`, or `flash-attn` wheel-build failures — even when the user does not explicitly ask for ZeroGPU coding guidance. Trigger on `import spaces` or `@spaces.GPU` in code.

This plugin packages the [`huggingface-zerogpu`](skills/huggingface-zerogpu/SKILL.md) skill from
[huggingface/skills](https://github.com/huggingface/skills/tree/main/skills/huggingface-zerogpu) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/huggingface-zerogpu/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install huggingface-zerogpu@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dhuggingface-zerogpu),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `huggingface-zerogpu`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[huggingface/skills](https://github.com/huggingface/skills).
