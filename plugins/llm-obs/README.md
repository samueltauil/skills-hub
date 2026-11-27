# llm-obs

Answer questions about LLM and agentic-application behavior from data already ingested into Elastic: latency and error rate, token and cost utilization, response quality and guardrail events, and agentic call-chain orchestration. Use when the user asks about LLM monitoring, GenAI observability, token spend or AI cost, model latency, prompt or guardrail failures, or how an agent's tool-call chain executed.

This plugin packages the [`observability-llm-obs`](skills/observability-llm-obs/SKILL.md) skill from
[elastic/agent-skills](https://github.com/elastic/agent-skills/tree/main/skills/observability/llm-obs) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/llm-obs/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install llm-obs@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dllm-obs),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `llm-obs`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[elastic/agent-skills](https://github.com/elastic/agent-skills).
