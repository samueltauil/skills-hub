# gemini-live-api

Builds, integrates, and troubleshoots Gemini Enterprise Agent Platform Live API (BidiGenerateContent) WebSocket clients and sessions. Use when scaffolding a LiveAPI client or demo UI/backend (GA v1 WebSockets, isolated Python venv, ADC bearer token refresh, transparent session resumption, ClientMessage and ServerMessage JSON protos, tool responses, context_update, interrupt and transcription handling) or debugging Live API issues such as silent or empty turns, audio amplitude collapse, tonal humming, voice gender or accent drift, premature turn completion, barge-in failures, output_transcription leaks, malformed or looping tool calls, WebSocket 1008/1011/goAway drops, or latency spikes. Don't use for non-live, non-bidirectional Gemini API calls such as unary generateContent, embeddings, image/video generation, or fine-tuning — use the gemini-api skill for those.

This plugin packages the [`gemini-live-api`](skills/gemini-live-api/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gemini-live-api) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gemini-live-api/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gemini-live-api@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgemini-live-api),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gemini-live-api`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
