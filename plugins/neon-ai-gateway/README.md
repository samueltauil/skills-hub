# neon-ai-gateway

One API and one credential for frontier and open-source LLMs and embedding models, built into your Neon branch and powered by Databricks. Use when a user wants to call an LLM, generate embeddings, add AI/chat/an agent to their app, route between model providers (OpenAI, Anthropic, Google/Gemini, Meta, Alibaba, and more), or avoid juggling separate provider API keys and accounts — especially when they already use Neon and want AI requests to branch with their project. Works with the OpenAI SDK, Anthropic SDK, google-genai, the Vercel AI SDK, and Mastra by changing only the base URL. Triggers include "call an LLM", "add AI to my app", "chat completion", "model routing", "LLM proxy/gateway", "one API for all models", "use Claude/GPT/Gemini", "AI SDK", "Mastra agent", "Neon AI Gateway", "generate embeddings", "generate images", and "log/rate-limit AI calls".

This plugin packages the [`neon-ai-gateway`](skills/neon-ai-gateway/SKILL.md) skill from
[neondatabase/agent-skills](https://github.com/neondatabase/agent-skills/tree/main/skills/neon-ai-gateway) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/neon-ai-gateway/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install neon-ai-gateway@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dneon-ai-gateway),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `neon-ai-gateway`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[neondatabase/agent-skills](https://github.com/neondatabase/agent-skills).
