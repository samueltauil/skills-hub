# gemini-api

Integrates Gemini models on Gemini platform (formerly Gemini Enterprise Agent Platform and Vertex AI) using the unified Google Gen AI SDK across Python, TypeScript/JavaScript, Go, Java, and C#. Use for Google Cloud AI workloads: text/multimodal generation, structured JSON, function calling, Search grounding, code execution, URL context, Nano Banana images, Gemini Omni and Veo video, TTS, Lyria music, embeddings, caching, batch, thinking, safety, Live API, or model tuning. Don't use for server-managed stateful agent sessions (gemini-interactions-api), Managed Agent CRUD (gemini-agents-api), raw BidiGenerateContent WebSocket scaffolding/audio debugging (gemini-live-api), open-model SFT or tuning job management (agent-platform-tuning, agent-platform-tuning-management), or OpenMaaS, OpenAI SDK, numeric endpoints, and 429 DSQ debugging (agent-platform-inference).

This plugin packages the [`gemini-api`](skills/gemini-api/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gemini-api) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gemini-api/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gemini-api@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgemini-api),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gemini-api`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
