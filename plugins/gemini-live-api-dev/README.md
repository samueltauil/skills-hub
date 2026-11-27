# gemini-live-api-dev

Use this skill when building real-time, bidirectional streaming applications with the Gemini Live API, or migrating legacy Live models (2.0/2.5/3.1) to Gemini 3.8 Live. Covers WebSocket-based audio/video/text streaming, voice activity detection (VAD), background reasoning (extended thinking), asynchronous function calling, session management, ephemeral tokens, live transcription, and live translation. SDKs covered - google-genai (Python), @google/genai (JavaScript/TypeScript).

This plugin packages the [`gemini-live-api-dev`](skills/gemini-live-api-dev/SKILL.md) skill from
[google-gemini/gemini-skills](https://github.com/google-gemini/gemini-skills/tree/main/skills/gemini-live-api-dev) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gemini-live-api-dev/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gemini-live-api-dev@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgemini-live-api-dev),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gemini-live-api-dev`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google-gemini/gemini-skills](https://github.com/google-gemini/gemini-skills).
