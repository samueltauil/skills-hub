# huggingface-lora-space-builder

Build and publish a Gradio demo on Hugging Face Spaces for a user-provided LoRA. Use when someone asks to create, generate, ship, or publish a Space, demo, Gradio app, or playground for a LoRA — including LoRAs for Qwen-Image, Qwen-Image-Edit, LTX-Video, Wan, FLUX, SDXL, or other diffusion base models. Also triggers when someone describes a LoRA they trained or hosts on the Hub and wants to share it. Covers picking the right base pipeline and `diffusers` inference recipe, designing a UI tailored to the LoRA's task and inputs (Union/multi-task control, edit, video, image, etc.), respecting model-card recommendations (trigger words, steps, guidance, LoRA scale, example inputs), and shipping to ZeroGPU hardware as a private Space by default.

This plugin packages the [`huggingface-lora-space-builder`](skills/huggingface-lora-space-builder/SKILL.md) skill from
[huggingface/skills](https://github.com/huggingface/skills/tree/main/skills/huggingface-lora-space-builder) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/huggingface-lora-space-builder/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install huggingface-lora-space-builder@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dhuggingface-lora-space-builder),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `huggingface-lora-space-builder`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[huggingface/skills](https://github.com/huggingface/skills).
