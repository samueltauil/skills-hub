# agent-platform-inference

Connects to and performs inference with Google Cloud Agent Platform GenAI models, including First-Party Gemini models and Third-Party OpenMaaS models (Llama, DeepSeek, Qwen, etc.). Use when asked to perform inference, ask a model a question, run a test prompt, execute chat completions, or generate code for calling Gemini or OpenMaaS models, authenticate with GenAI SDK, OpenAI SDK, or legacy Agent Platform SDK, configure base URLs and global/regional endpoints, or troubleshoot 429 Resource Exhausted (DSQ), 400 User Validation, or 404 Not Found errors. Don't use for deploying models to endpoints or for running model evaluations.

This plugin packages the [`agent-platform-inference`](skills/agent-platform-inference/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/agent-platform-inference) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/agent-platform-inference/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install agent-platform-inference@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dagent-platform-inference),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `agent-platform-inference`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
