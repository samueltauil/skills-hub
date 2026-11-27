# gemini-api-dev

Use this skill when writing code that calls the Gemini API for text generation, multi-turn chat, multimodal understanding, image generation, video generation, speech generation (TTS), voice design, voice replication, streaming responses, background research tasks, function calling, structured output, calibrated decisions (yes/no, choice, rubric scoring), or migrating from the old generateContent API. Covers SDK usage and best practices for Gemini models and agents in Python and TypeScript.

This plugin packages the [`gemini-api-dev`](skills/gemini-api-dev/SKILL.md) skill from
[google-gemini/gemini-skills](https://github.com/google-gemini/gemini-skills/tree/main/skills/gemini-api-dev) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gemini-api-dev/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gemini-api-dev@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgemini-api-dev),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gemini-api-dev`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google-gemini/gemini-skills](https://github.com/google-gemini/gemini-skills).
