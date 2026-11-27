# prompt-optimizer

Turn any rough prompt, half-formed idea, or task description into a finished, ready-to-send prompt optimized for any LLM model inside a chat interface — NOT the API. Use this skill whenever the user wants to write, rewrite, optimize, improve, sharpen, or polish a prompt for chat. Trigger phrases include "rewrite this prompt", "make this a better prompt", "optimize this prompt", "turn this into a prompt", "help me prompt this", "draft a prompt that...", "I want to ask...", or whenever the user pastes a draft prompt and asks for improvements. Also trigger when the user describes a task they plan to send to an LLM model and clearly wants a reusable, well-structured prompt rather than a direct answer. The output is always a single, copy-pasteable prompt in a code block that the user sends as-is — never a template with placeholders.

This plugin packages the [`prompt-optimizer`](skills/prompt-optimizer/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/prompt-optimizer) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/prompt-optimizer/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install prompt-optimizer@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dprompt-optimizer),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `prompt-optimizer`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
