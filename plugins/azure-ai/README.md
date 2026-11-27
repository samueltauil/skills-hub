# azure-ai

Build and troubleshoot Azure AI Search, Speech, Document Intelligence, Content Understanding, Translator, Content Safety, and OpenAI apps. WHEN: AI Search, vector search, hybrid search, semantic search, indexer, speech-to-text, text-to-speech, fast or batch transcription, Speech SDK logs, session ID, result ID, OCR, document translation, glossary.

This plugin packages the [`azure-ai`](skills/azure-ai/SKILL.md) skill from
[microsoft/azure-skills](https://github.com/microsoft/azure-skills/tree/main/.github/plugins/azure-skills/skills/azure-ai) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/azure-ai/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install azure-ai@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dazure-ai),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `azure-ai`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[microsoft/azure-skills](https://github.com/microsoft/azure-skills).
