# huggingface-spaces

Build, deploy, and maintain applications on Hugging Face Spaces — Gradio / Docker / Static SDKs, ZeroGPU and dedicated hardware, model loading, debugging, buckets, inference providers, community grants. Use whenever the user asks to create or host an app on Hugging Face, port code onto ZeroGPU, fix a Space that won't build or run, or otherwise work with `hf spaces …`, `@spaces.GPU`, Space README frontmatter, or the `spaces` Python package.

This plugin packages the [`huggingface-spaces`](skills/huggingface-spaces/SKILL.md) skill from
[huggingface/skills](https://github.com/huggingface/skills/tree/main/skills/huggingface-spaces) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/huggingface-spaces/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install huggingface-spaces@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dhuggingface-spaces),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `huggingface-spaces`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[huggingface/skills](https://github.com/huggingface/skills).
