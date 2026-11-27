# transformers-js

Use Transformers.js to run state-of-the-art machine learning models directly in JavaScript/TypeScript. Supports NLP (text classification, translation, summarization), computer vision (image classification, object detection), audio (speech recognition, audio classification), and multimodal tasks. Works in browsers and server-side runtimes (Node.js, Bun, Deno) with WebGPU/WASM using pre-trained models from Hugging Face Hub.

This plugin packages the [`transformers-js`](skills/transformers-js/SKILL.md) skill from
[huggingface/skills](https://github.com/huggingface/skills/tree/main/skills/transformers-js) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/transformers-js/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install transformers-js@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dtransformers-js),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `transformers-js`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[huggingface/skills](https://github.com/huggingface/skills).
