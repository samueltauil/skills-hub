# arize-ai-provider-integration

Creates, reads, updates, and deletes Arize AI integrations that store LLM provider credentials used by evaluators and other Arize features. Supports any LLM provider (e.g. OpenAI, Anthropic, Azure OpenAI, AWS Bedrock, Vertex AI, Gemini, NVIDIA NIM). Use when the user mentions AI integration, LLM provider credentials, create integration, list integrations, update credentials, delete integration, or connecting an LLM provider to Arize.

This plugin packages the [`arize-ai-provider-integration`](skills/arize-ai-provider-integration/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/arize-ai-provider-integration) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/arize-ai-provider-integration/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install arize-ai-provider-integration@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Darize-ai-provider-integration),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `arize-ai-provider-integration`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
